"""Autenticação e registo de alunos."""
from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

from . import routes  # noqa: E402,F401  (regista as rotas no blueprint)
