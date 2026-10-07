"""Área de gestão (US03): administradores independentes dos alunos.

O endereço da área vem de ``ADMIN_URL_PREFIX`` (por omissão ``/gestao``) e nenhuma página
dos alunos tem ligações para ela.
"""
from flask import Blueprint

bp = Blueprint("gestao", __name__)

from . import routes, sessions  # noqa: E402,F401  (regista as rotas no blueprint)

bp.before_app_request(sessions.load_current_admin)
