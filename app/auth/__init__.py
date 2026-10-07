"""Autenticação e registo de alunos."""
from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

from . import routes, sessions  # noqa: E402,F401  (regista as rotas no blueprint)

bp.before_app_request(sessions.load_current_user)
