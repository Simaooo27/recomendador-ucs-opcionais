"""Páginas das decisões do percurso (US31): /percurso.

- ``GET /percurso/``: a linha do tempo das decisões (RF35).
- ``GET /percurso/escolher/<chave>``: confirmar a escolha (RN10: nada é escolhido sem confirmar).
- ``POST /percurso/escolher/<chave>``: regista a escolha.

As rotas só recebem o pedido e mostram a página; as regras estão em ``services.py``.
"""
from __future__ import annotations

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, url_for

from .. import texts
from ..auth.sessions import login_required
from ..catalogo import services as catalogo
from ..db import get_db
from . import services

bp = Blueprint("percurso", __name__, url_prefix="/percurso")


def _curso_ou_404(chave: str):
    try:
        return services.curso_do_catalogo(chave, catalogo.cursos(current_app.config))
    except services.CursoInexistente:
        abort(404)


@bp.get("/")
@login_required
def linha_tempo():
    return render_template("percurso/linha_tempo.html", decisoes=services.decisoes(get_db(), g.user["id"]))


@bp.get("/escolher/<chave>")
@login_required
def confirmar(chave: str):
    curso = _curso_ou_404(chave)
    return render_template("percurso/escolher.html", curso=curso, atual=services.curso_atual(get_db(), g.user["id"]))


@bp.post("/escolher/<chave>")
@login_required
def escolher(chave: str):
    _curso_ou_404(chave)
    try:
        decisao = services.escolher(get_db(), g.user["id"], chave, catalogo.cursos(current_app.config))
    except services.MesmoCurso:
        flash(texts.PERCURSO_JA_E_O_SEU_CURSO, "error")
        return redirect(url_for("percurso.linha_tempo"))
    flash(texts.PERCURSO_ESCOLHA_REGISTADA.format(curso=decisao.curso, instituicao=decisao.instituicao), "ok")
    return redirect(url_for("percurso.linha_tempo"))
