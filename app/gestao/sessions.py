"""Sessão dos administradores (US03), separada da sessão dos alunos."""
from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import g, redirect, session, url_for

from ..db import get_db
from . import repository

_ADMIN_ID_KEY = "admin_id"


def load_current_admin() -> None:
    """Carrega ``g.admin`` a partir da sessão (antes de cada pedido)."""
    g.admin = None
    admin_id = session.get(_ADMIN_ID_KEY)
    if admin_id is None:
        return
    admin = repository.get_by_id(get_db(), admin_id)
    if admin is None:  # foi removido entretanto
        session.clear()
        return
    g.admin = admin


def login_admin(admin_id: int) -> None:
    """Começa uma sessão nova só de administrador (termina uma eventual sessão de aluno)."""
    session.clear()
    session[_ADMIN_ID_KEY] = admin_id


def logout_admin() -> None:
    session.clear()


def admin_required(view: Callable) -> Callable:
    """Páginas da área de gestão: sem sessão de administrador, vai para o início de sessão da gestão."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.get("admin") is None:
            return redirect(url_for("gestao.login_form"))
        return view(*args, **kwargs)

    return wrapped
