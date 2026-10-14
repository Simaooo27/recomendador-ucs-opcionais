"""Catálogo de cursos (US04, US05).

Por agora o catálogo é lido do ficheiro dados/catalogo-cursos-mvp.csv (repository.py).
Quando a US04 importar o catálogo para a base de dados, só o repository muda: os
serviços e as páginas continuam a receber os mesmos objetos ``Curso`` (padrão Repository).
"""
from flask import Blueprint

bp = Blueprint("catalogo", __name__, url_prefix="/cursos")

from . import routes  # noqa: E402,F401  (regista as rotas no blueprint)
