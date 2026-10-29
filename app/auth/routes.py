"""Rotas HTTP do registo (US01) e do início e fim de sessão (US02)."""
from __future__ import annotations

from flask import current_app, flash, g, redirect, render_template, request, session, url_for

from .. import texts
from ..db import get_db
from ..mailer import Message
from . import bp, services, sessions
from .perfis import criar_cadeia_de_perfis
from .services import ConfirmationOutcome, LoginOutcome, RecuperacaoOutcome
from .validators import RegistrationInput, domains_hint, is_valid_email, normalize_email, primeiro_nome

_PENDING_EMAIL_KEY = "pending_email"
# Só em desenvolvimento (MAIL_BACKEND=console): a ligação aparece também na página.
_DEV_LINK_KEY = "dev_confirmation_link"

_CONFIRMATION_STATUS = {
    ConfirmationOutcome.CONFIRMED: 200,
    ConfirmationOutcome.ALREADY_CONFIRMED: 200,
    ConfirmationOutcome.INVALID: 400,
    ConfirmationOutcome.EXPIRED: 410,
}

MSG_EMAIL_SEND_FAILED = texts.ERROR_EMAIL_SEND_FAILED


def _render_register(values: dict, errors: dict, status: int = 200):
    page = render_template(
        "auth/register.html",
        values=values,
        errors=errors,
        domains_hint=domains_hint(current_app.config["ALLOWED_EMAIL_DOMAINS"]),
        min_length=current_app.config["PASSWORD_MIN_LENGTH"],
    )
    return page, status


def _confirmation_message(to: str, link: str, nome: str = "") -> Message:
    hours = current_app.config["CONFIRMATION_TOKEN_MAX_AGE_SECONDS"] // 3600
    saudacao = texts.CONFIRMATION_EMAIL_HELLO_NOME.format(nome=primeiro_nome(nome)) if nome else texts.CONFIRMATION_EMAIL_HELLO
    body = saudacao + texts.CONFIRMATION_EMAIL_BODY.format(horas=hours, ligacao=link)
    return Message(to=to, subject=texts.CONFIRMATION_EMAIL_SUBJECT, body=body)


@bp.get("/registo")
def register_form():
    return _render_register(values={}, errors={})


@bp.post("/registo")
def register_submit():
    data = RegistrationInput(
        nome=request.form.get("nome", ""),
        email=request.form.get("email", ""),
        password=request.form.get("password", ""),
        password_confirm=request.form.get("password_confirm", ""),
        accepted_privacy=request.form.get("accepted_privacy") == "on",
    )
    try:
        pending = services.register_student(get_db(), data, current_app.config)
    except services.RegistrationRejected as rejected:
        # A palavra-passe nunca volta ao navegador; o email sim, para não o reescrever.
        return _render_register(values={"email": data.email, "nome": data.nome}, errors=rejected.errors, status=422)

    link = url_for("auth.confirm", token=pending.token, _external=True)
    try:
        current_app.extensions["mailer"].send(_confirmation_message(pending.email, link, pending.nome))
    except Exception:  # noqa: BLE001 - qualquer falha de envio deve ser tratada igual
        current_app.logger.exception("Falha ao enviar o email de confirmação")
        return _render_register(
            values={"email": pending.email, "nome": pending.nome}, errors={"form": MSG_EMAIL_SEND_FAILED}, status=503
        )

    session[_PENDING_EMAIL_KEY] = pending.email
    # A ligação só vai para a sessão se for para a mostrar: o cookie de sessão é assinado, mas
    # o navegador consegue lê-lo, por isso guardá-la ali bastava para confirmar qualquer email.
    if _mostrar_ligacao_de_desenvolvimento():
        session[_DEV_LINK_KEY] = link
    else:
        session.pop(_DEV_LINK_KEY, None)
    return redirect(url_for("auth.register_pending"))


def _mostrar_ligacao_de_desenvolvimento() -> bool:
    """Em desenvolvimento (email no terminal), a ligação de confirmação aparece também na página."""
    return current_app.config["MAIL_BACKEND"] == "console" and current_app.config["SHOW_DEV_CONFIRMATION_LINK"]


@bp.get("/registo/pendente")
def register_pending():
    dev_link = session.get(_DEV_LINK_KEY) if _mostrar_ligacao_de_desenvolvimento() else None
    return render_template("auth/pending.html", email=session.get(_PENDING_EMAIL_KEY), dev_link=dev_link)


@bp.get("/confirmar/<token>")
def confirm(token: str):
    outcome = services.confirm_email(get_db(), token, current_app.config)
    response = current_app.make_response(
        (render_template("auth/confirmation.html", outcome=outcome.value), _CONFIRMATION_STATUS[outcome])
    )
    response.headers["Cache-Control"] = "no-store"
    return response


# -- US02 e US03: iniciar e terminar sessão (alunos e administradores) -------------------------------------------------

_LOGIN_ERRORS = {
    LoginOutcome.INVALID_CREDENTIALS: (texts.ERROR_LOGIN_INVALID, 401),
    LoginOutcome.INACTIVE: (texts.ERROR_LOGIN_INACTIVE, 403),
}


def _render_login(email: str = "", error: str | None = None, status: int = 200):
    return render_template("auth/login.html", email=email, error=error), status


@bp.get("/entrar")
def login_form():
    if g.user is not None:
        return redirect(url_for("main.home"))
    if g.get("admin") is not None:
        return redirect(url_for("gestao.dashboard"))
    return _render_login()


@bp.post("/entrar")
def login_submit():
    """Um só início de sessão: a cadeia de perfis decide se é aluno ou administrador (app/auth/perfis.py)."""
    identificador = request.form.get("email", "")
    entrada = criar_cadeia_de_perfis().entrar(get_db(), identificador, request.form.get("password", ""))
    if entrada.outcome is LoginOutcome.SUCCESS:
        entrada.perfil.iniciar_sessao(entrada.conta_id)
        return redirect(url_for(entrada.perfil.pagina_inicial))
    message, status = _LOGIN_ERRORS[entrada.outcome]
    # A palavra-passe nunca volta ao navegador; o identificador sim, para não o reescrever.
    return _render_login(email=identificador.strip(), error=message, status=status)


@bp.post("/sair")
def logout():
    """Termina a sessão e volta à página inicial (a apresentação), não ao login (decisão do PO, 23/10)."""
    sessions.logout_user()
    flash(texts.LOGOUT_FEITO, "ok")
    return redirect(url_for("main.index"))


# ---------------------------------------------------------------------------
# Recuperar a palavra-passe (US47)
# ---------------------------------------------------------------------------

_RECUPERACAO_STATUS = {RecuperacaoOutcome.INVALID: 400, RecuperacaoOutcome.EXPIRED: 410}


def _recovery_message(to: str, link: str, nome: str) -> Message:
    minutos = current_app.config["RESET_TOKEN_MAX_AGE_SECONDS"] // 60
    saudacao = texts.CONFIRMATION_EMAIL_HELLO_NOME.format(nome=primeiro_nome(nome)) if nome else texts.CONFIRMATION_EMAIL_HELLO
    body = saudacao + texts.RECUPERAR_EMAIL_BODY.format(minutos=minutos, ligacao=link)
    return Message(to=to, subject=texts.RECUPERAR_EMAIL_SUBJECT, body=body)


def _no_store(page, status: int):
    # A ligação leva o token no endereço: a página não fica guardada em caches.
    response = current_app.make_response((page, status))
    response.headers["Cache-Control"] = "no-store"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@bp.get("/recuperar")
def recovery_form():
    return render_template("auth/recuperar.html", email="", error=None)


@bp.post("/recuperar")
def recovery_submit():
    """Envia a ligação, se houver conta ativa. A resposta é a mesma quer a conta exista quer não."""
    email = normalize_email(request.form.get("email", ""))
    if not is_valid_email(email):
        # Só o formato: não diz nada sobre se a conta existe.
        return render_template("auth/recuperar.html", email=email, error=texts.ERROR_EMAIL_INVALID), 422
    pedido = services.pedir_recuperacao(get_db(), email, current_app.config)
    if pedido is not None:
        link = url_for("auth.recovery_reset_form", token=pedido.token, _external=True)
        try:
            current_app.extensions["mailer"].send(_recovery_message(pedido.email, link, pedido.nome))
        except Exception:  # noqa: BLE001 - mostrar um erro aqui revelaria que a conta existe
            current_app.logger.exception("Falha ao enviar o email de recuperação da palavra-passe")
    # A ligação nunca aparece na página (ao contrário da confirmação em desenvolvimento): quem
    # pedisse a recuperação de uma conta que não é sua podia mudar-lhe a palavra-passe.
    return redirect(url_for("auth.recovery_sent"))


@bp.get("/recuperar/enviado")
def recovery_sent():
    return render_template("auth/recuperar_enviado.html")


@bp.get("/recuperar/<token>")
def recovery_reset_form(token: str):
    outcome = services.verificar_recuperacao(get_db(), token, current_app.config)
    if outcome is not RecuperacaoOutcome.VALID:
        return _no_store(render_template("auth/recuperar_ligacao.html", outcome=outcome.value), _RECUPERACAO_STATUS[outcome])
    page = render_template(
        "auth/recuperar_nova.html", token=token, errors={}, min_length=current_app.config["PASSWORD_MIN_LENGTH"]
    )
    return _no_store(page, 200)


@bp.post("/recuperar/<token>")
def recovery_reset_submit(token: str):
    try:
        outcome = services.recuperar_password(
            get_db(), token, request.form.get("password", ""), request.form.get("password_confirm", ""), current_app.config
        )
    except services.RecuperacaoRejeitada as rejected:
        page = render_template(
            "auth/recuperar_nova.html", token=token, errors=rejected.errors, min_length=current_app.config["PASSWORD_MIN_LENGTH"]
        )
        return _no_store(page, 422)
    if outcome is not RecuperacaoOutcome.VALID:
        return _no_store(render_template("auth/recuperar_ligacao.html", outcome=outcome.value), _RECUPERACAO_STATUS[outcome])
    # Termina também a sessão deste navegador, se houver: entra-se de novo com a palavra-passe nova.
    sessions.logout_user()
    flash(texts.RECUPERAR_FEITO, "ok")
    return redirect(url_for("auth.login_form"))


# ---------------------------------------------------------------------------
# Apagar a minha conta (US17)
# ---------------------------------------------------------------------------

def _render_conta(nome: str | None = None, erro_nome: str | None = None, status: int = 200):
    criada = (g.user["created_at"] or "")[:10]          # AAAA-MM-DD (UTC)
    criada = "/".join(reversed(criada.split("-"))) if criada else ""
    nome = g.user["nome"] if nome is None else nome
    return render_template("auth/conta.html", criada=criada, nome=nome, erro_nome=erro_nome), status


@bp.get("/conta")
@sessions.login_required
def account():
    """«A minha conta» (revisão de 23/10): nome, email, data de criação e a ligação para apagar a conta."""
    return _render_conta()


@bp.post("/conta/nome")
@sessions.login_required
def change_nome():
    """Muda o nome com que o OptaBem trata a pessoa (também para contas criadas antes de 23/10)."""
    nome = request.form.get("nome", "")
    erro = services.change_nome(get_db(), g.user["id"], nome)
    if erro:
        return _render_conta(nome=nome, erro_nome=erro, status=422)
    flash(texts.CONTA_NOME_GUARDADO, "ok")
    return redirect(url_for("auth.account"))


def _render_apagar(error: str | None = None, status: int = 200):
    return render_template("auth/apagar.html", error=error), status


@bp.get("/conta/apagar")
@sessions.login_required
def delete_account_form():
    return _render_apagar()


@bp.post("/conta/apagar")
@sessions.login_required
def delete_account_submit():
    """Apaga a conta depois de confirmada com a palavra-passe; termina a sessão."""
    if not services.delete_account(get_db(), g.user["id"], request.form.get("password", "")):
        return _render_apagar(texts.APAGAR_ERRO_PASSWORD, 422)
    sessions.logout_user()
    flash(texts.APAGAR_FEITO, "ok")
    return redirect(url_for("main.index"))
