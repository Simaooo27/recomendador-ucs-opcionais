"""Rotas da área de gestão (US03)."""
from __future__ import annotations

from flask import current_app, flash, g, redirect, render_template, request, url_for

from .. import texts
from ..db import get_db
from . import bp, repository, services, sessions
from .services import RemoveOutcome


@bp.get("/entrar")
def login_form():
    if g.admin is not None:
        return redirect(url_for("gestao.dashboard"))
    return render_template("gestao/login.html", username="", error=None)


@bp.post("/entrar")
def login_submit():
    username = request.form.get("username", "")
    admin_id = services.authenticate(get_db(), username, request.form.get("password", ""))
    if admin_id is None:
        page = render_template("gestao/login.html", username=username.strip(), error=texts.ERROR_ADMIN_LOGIN_INVALID)
        return page, 401
    sessions.login_admin(admin_id)
    return redirect(url_for("gestao.dashboard"))


@bp.post("/sair")
def logout():
    sessions.logout_admin()
    return redirect(url_for("gestao.login_form"))


@bp.get("/")
@sessions.admin_required
def dashboard():
    return render_template("gestao/painel.html")


def _render_admins(values: dict | None = None, errors: dict | None = None, status: int = 200):
    page = render_template(
        "gestao/administradores.html",
        admins=repository.list_all(get_db()),
        values=values or {},
        errors=errors or {},
        min_length=current_app.config["PASSWORD_MIN_LENGTH"],
    )
    return page, status


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
