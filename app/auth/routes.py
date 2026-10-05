"""Rotas HTTP do registo (US01)."""
from __future__ import annotations

from flask import current_app, redirect, render_template, request, session, url_for

from ..db import get_db
from ..mailer import Message
from . import bp, services
from .services import ConfirmationOutcome
from .validators import RegistrationInput

_PENDING_EMAIL_KEY = "pending_email"

_CONFIRMATION_STATUS = {
    ConfirmationOutcome.CONFIRMED: 200,
    ConfirmationOutcome.ALREADY_CONFIRMED: 200,
    ConfirmationOutcome.INVALID: 400,
    ConfirmationOutcome.EXPIRED: 410,
}

MSG_EMAIL_SEND_FAILED = (
    "Não foi possível enviar o email de confirmação. Tente de novo dentro de alguns minutos."
)


def _render_register(values: dict, errors: dict, status: int = 200):
    domains = current_app.config["ALLOWED_EMAIL_DOMAINS"]
    page = render_template(
        "auth/register.html",
        values=values,
        errors=errors,
        domains_hint=" ou ".join("@" + d for d in domains),
        min_length=current_app.config["PASSWORD_MIN_LENGTH"],
    )
    return page, status


def _confirmation_message(to: str, link: str) -> Message:
    hours = current_app.config["CONFIRMATION_TOKEN_MAX_AGE_SECONDS"] // 3600
    body = (
        "Olá,\n\n"
        "Recebemos um pedido de registo com este email. Para ativar a conta, abra a "
        f"ligação abaixo nas próximas {hours} horas:\n\n"
        f"{link}\n\n"
        "Se não fez este pedido, ignore esta mensagem: a conta não será ativada.\n"
    )
    return Message(to=to, subject="Confirme o seu registo", body=body)


@bp.get("/registo")
def register_form():
    return _render_register(values={}, errors={})


@bp.post("/registo")
def register_submit():
    data = RegistrationInput(
        email=request.form.get("email", ""),
        password=request.form.get("password", ""),
        password_confirm=request.form.get("password_confirm", ""),
        accepted_privacy=request.form.get("accepted_privacy") == "on",
    )
    try:
        pending = services.register_student(get_db(), data, current_app.config)
    except services.RegistrationRejected as rejected:
        # A palavra-passe nunca volta ao navegador; o email sim, para não o reescrever.
        return _render_register(values={"email": data.email}, errors=rejected.errors, status=422)

    link = url_for("auth.confirm", token=pending.token, _external=True)
    try:
        current_app.extensions["mailer"].send(_confirmation_message(pending.email, link))
    except Exception:  # noqa: BLE001 - qualquer falha de envio deve ser tratada igual
        current_app.logger.exception("Falha ao enviar o email de confirmação")
        return _render_register(
            values={"email": pending.email}, errors={"form": MSG_EMAIL_SEND_FAILED}, status=503
        )

    session[_PENDING_EMAIL_KEY] = pending.email
    return redirect(url_for("auth.register_pending"))


@bp.get("/registo/pendente")
def register_pending():
    return render_template("auth/pending.html", email=session.get(_PENDING_EMAIL_KEY))


@bp.get("/confirmar/<token>")
def confirm(token: str):
    outcome = services.confirm_email(get_db(), token, current_app.config)
    response = current_app.make_response(
        (render_template("auth/confirmation.html", outcome=outcome.value), _CONFIRMATION_STATUS[outcome])
    )
    response.headers["Cache-Control"] = "no-store"
    return response
