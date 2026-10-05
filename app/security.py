"""Proteção CSRF e cabeçalhos de segurança."""
from __future__ import annotations

import hmac
import secrets

from flask import Flask, Response, abort, request, session

CSRF_SESSION_KEY = "csrf_token"
CSRF_FIELD_NAME = "csrf_token"
_UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def get_csrf_token() -> str:
    """Devolve o token CSRF da sessão, criando-o se necessário."""
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
    return token


def _check_csrf() -> None:
    if request.method not in _UNSAFE_METHODS:
        return
    expected = session.get(CSRF_SESSION_KEY, "")
    sent = request.form.get(CSRF_FIELD_NAME, "")
    if not expected or not hmac.compare_digest(sent.encode(), expected.encode()):
        abort(400, description="Pedido inválido ou expirado. Recarregue a página e tente de novo.")


def _security_headers(response: Response) -> Response:
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    # A ligação de confirmação contém um token: não pode viajar em Referer.
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    return response


def init_security(app: Flask) -> None:
    app.before_request(_check_csrf)
    app.after_request(_security_headers)
    app.jinja_env.globals["csrf_token"] = get_csrf_token
    app.jinja_env.globals["csrf_field_name"] = CSRF_FIELD_NAME
