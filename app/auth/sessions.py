"""Sessão do utilizador: quem está autenticado, entrar, sair e páginas privadas (US02).

Este módulo é a única parte do código que guarda ou lê o utilizador na sessão.
"""
from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import g, redirect, session, url_for

from ..db import get_db
from . import repository

_USER_ID_KEY = "user_id"


def load_current_user() -> None:
    """Carrega ``g.user`` a partir da sessão (antes de cada pedido).

    Se a conta deixou de existir ou não está ativa, a sessão é limpa.
    """
    g.user = None
    user_id = session.get(_USER_ID_KEY)
    if user_id is None:
        return
    user = repository.get_by_id(get_db(), user_id)
    if user is None or not user["is_active"]:
        session.clear()
        return
    g.user = user


def login_user(user_id: int) -> None:
    """Inicia sessão. Começa uma sessão nova para impedir a fixação de sessão."""
    session.clear()
    session[_USER_ID_KEY] = user_id


def logout_user() -> None:
    session.clear()


def login_required(view: Callable) -> Callable:
    """Decorador para páginas privadas: sem sessão, redireciona para o início de sessão."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.get("user") is None:
            return redirect(url_for("auth.login_form"))
        return view(*args, **kwargs)

    return wrapped
