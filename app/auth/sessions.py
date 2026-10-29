"""Sessão do utilizador: quem está autenticado, entrar, sair e páginas privadas (US02).

Este módulo é a única parte do código que guarda ou lê o utilizador na sessão.
"""
from __future__ import annotations

from functools import wraps
from typing import Callable

import hmac

from flask import current_app, g, redirect, session, url_for

from ..db import get_db
from . import repository
from .tokens import impressao_da_password

_USER_ID_KEY = "user_id"
# Impressão da palavra-passe no momento em que a sessão começou (US47): se a palavra-passe mudar,
# todas as sessões abertas dessa conta terminam no pedido seguinte.
_PASSWORD_KEY = "pw"


def _impressao(user) -> str:
    return impressao_da_password(current_app.config["SECRET_KEY"], user["password_hash"])


def load_current_user() -> None:
    """Carrega ``g.user`` a partir da sessão (antes de cada pedido).

    Se a conta deixou de existir, não está ativa ou a palavra-passe mudou depois de a sessão
    começar (US47), a sessão é limpa.
    """
    g.user = None
    user_id = session.get(_USER_ID_KEY)
    if user_id is None:
        return
    user = repository.get_by_id(get_db(), user_id)
    if user is None or not user["is_active"] or not hmac.compare_digest(
        str(session.get(_PASSWORD_KEY, "")), _impressao(user)
    ):
        session.clear()
        return
    g.user = user


def login_user(user_id: int) -> None:
    """Inicia sessão. Começa uma sessão nova para impedir a fixação de sessão."""
    session.clear()
    session[_USER_ID_KEY] = user_id
    user = repository.get_by_id(get_db(), user_id)
    if user is not None:
        session[_PASSWORD_KEY] = _impressao(user)


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
