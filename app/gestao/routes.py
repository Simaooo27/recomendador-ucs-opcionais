"""Rotas da área de gestão (US03)."""
from __future__ import annotations

from flask import abort, current_app, flash, g, redirect, render_template, request, url_for

from .. import texts
from ..db import get_db
from . import bp, repository, services, sessions
from .services import RemoveOutcome


@bp.get("/entrar")
def login_form():
    """Endereço antigo: o início de sessão é o mesmo para todos (app/auth/perfis.py)."""
    return redirect(url_for("auth.login_form"))


@bp.get("/")
@sessions.admin_required
def dashboard():
    return render_template("gestao/painel.html", indicadores=services.indicadores(get_db()))


def _render_admins(values: dict | None = None, errors: dict | None = None, status: int = 200):
    page = render_template(
        "gestao/administradores.html",
        admins=repository.list_all(get_db()),
        values=values or {},
        errors=errors or {},
        min_length=current_app.config["PASSWORD_MIN_LENGTH"],
    )
    return page, status


@bp.get("/contas")
@sessions.admin_required
def contas():
    """Contas de alunos por confirmar, com o botão «Ativar» (23/10: o site ainda não envia emails reais)."""
    from ..auth import repository as contas_alunos

    return render_template("gestao/contas.html", pendentes=contas_alunos.list_pending(get_db()))


@bp.post("/contas/<int:user_id>/ativar")
@sessions.admin_required
def contas_ativar(user_id: int):
    email = services.ativar_conta(get_db(), user_id)
    if email:
        flash(texts.ADMIN_CONTA_ATIVADA.format(email=email), "ok")
    return redirect(url_for("gestao.contas"))


@bp.get("/administradores")
@sessions.admin_required
def admins():
    return _render_admins()


@bp.post("/administradores")
@sessions.admin_required
def admins_create():
    username = request.form.get("username", "")
    try:
        services.create_admin(
            get_db(),
            username,
            request.form.get("password", ""),
            request.form.get("password_confirm", ""),
            current_app.config,
            created_by=g.admin["username"],
        )
    except services.AdminRejected as rejected:
        return _render_admins(values={"username": username.strip()}, errors=rejected.errors, status=422)
    flash(texts.ADMIN_CREATED.format(nome=services.normalize_username(username)), "ok")
    return redirect(url_for("gestao.admins"))


@bp.post("/administradores/<int:admin_id>/remover")
@sessions.admin_required
def admins_remove(admin_id: int):
    result = services.remove_admin(get_db(), admin_id, removed_by=int(g.admin["id"]))
    if result.outcome is RemoveOutcome.REMOVED:
        flash(texts.ADMIN_REMOVED.format(nome=result.username), "ok")
    elif result.outcome is RemoveOutcome.SELF:
        flash(texts.ERROR_ADMIN_REMOVE_SELF, "error")
    return redirect(url_for("gestao.admins"))


# ---------------------------------------------------------------------------
# Catálogo: corrigir e esconder cursos (US39). Só cursos; nenhuma destas páginas lê dados de alunos.
# ---------------------------------------------------------------------------

_FILTROS_CURSOS = ("todos", "corrigidos", "escondidos")


@bp.get("/cursos")
@sessions.admin_required
def cursos():
    from ..catalogo import services as catalogo

    termo = request.args.get("q", "")[:80]
    mostrar = request.args.get("mostrar", "todos")
    mostrar = mostrar if mostrar in _FILTROS_CURSOS else "todos"
    linhas = [
        (curso, correcao)
        for curso, correcao in catalogo.cursos_para_gestao(current_app.config, get_db())
        if catalogo.corresponde(curso, termo)
        and (mostrar == "todos" or (correcao is not None and (mostrar == "corrigidos" or correcao.escondido)))
    ]
    linhas.sort(key=lambda par: (par[0].curso, par[0].instituicao))
    return render_template("gestao/cursos.html", linhas=linhas, termo=termo, mostrar=mostrar)


def _render_curso(chave: str, *, valores: dict | None = None, errors: dict | None = None, status: int = 200):
    from ..catalogo import repository as catalogo_repository
    from ..catalogo import services as catalogo

    original = next((c for c in catalogo_repository.todos(current_app.config["CATALOGO_CSV"]) if c.chave == chave), None)
    if original is None:
        abort(404)
    correcao = catalogo.correcoes(get_db()).get(chave)
    atual = catalogo.corrigido(original, correcao)
    if valores is None:
        # Uma saída por linha, tal como estão escritas (sem a maiúscula que a ficha lhes põe): guardar o
        # formulário sem mexer nas saídas não pode criar uma correção.
        saidas = "\n".join(p.strip() for p in atual.saidas.split(";") if p.strip())
        valores = {"descricao": atual.descricao, "saidas": saidas, "escondido": bool(correcao and correcao.escondido)}
    page = render_template(
        "gestao/curso.html",
        original=original,
        correcao=correcao,
        valores=valores,
        errors=errors or {},
        historico=services.historico_do_curso(get_db(), chave),
        limites={"descricao": services.LIMITE_DESCRICAO, "saidas": services.LIMITE_SAIDAS},
    )
    return page, status


@bp.get("/cursos/<chave>")
@sessions.admin_required
def curso(chave: str):
    return _render_curso(chave)


@bp.post("/cursos/<chave>")
@sessions.admin_required
def curso_guardar(chave: str):
    valores = {
        "descricao": request.form.get("descricao", ""),
        "saidas": request.form.get("saidas", ""),
        "escondido": request.form.get("escondido") == "on",
    }
    try:
        mudou = services.guardar_correcao(get_db(), current_app.config, chave, admin=g.admin["username"], **valores)
    except services.CursoInexistente:
        abort(404)
    except services.CorrecaoRejeitada as rejected:
        return _render_curso(chave, valores=valores, errors=rejected.errors, status=422)
    flash(texts.ADMIN_CURSO_GUARDADO if mudou else texts.ADMIN_CURSO_NADA_MUDOU, "ok")
    return redirect(url_for("gestao.curso", chave=chave))


@bp.post("/cursos/<chave>/repor")
@sessions.admin_required
def curso_repor(chave: str):
    try:
        reposto = services.repor_curso(get_db(), current_app.config, chave, admin=g.admin["username"])
    except services.CursoInexistente:
        abort(404)
    flash(texts.ADMIN_CURSO_REPOSTO if reposto else texts.ADMIN_CURSO_NADA_MUDOU, "ok")
    return redirect(url_for("gestao.curso", chave=chave))
