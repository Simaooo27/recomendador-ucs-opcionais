"""Páginas gerais."""
from flask import Blueprint, current_app, g, redirect, render_template, request, url_for

from . import percurso
from .catalogo import services as catalogo
from .auth.sessions import login_required
from .db import get_db
from .orientacao import services as orientacao_services

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    """Com sessão iniciada vai para a área de cada perfil; sem sessão, mostra a apresentação."""
    if g.user is not None:
        return redirect(url_for("main.home"))
    if g.get("admin") is not None:
        return redirect(url_for("gestao.dashboard"))
    termo = request.args.get("q", "")[:80]
    return render_template(
        "landing.html",
        termo=termo,
        resultado=catalogo.pesquisar(current_app.config, termo),
        resumo=catalogo.resumo(current_app.config),
    )


@bp.get("/inicio")
@login_required
def home():
    terminada = orientacao_services.tem_sugestao(get_db(), g.user["id"])
    estado = percurso.estado_do_utilizador(g.user, conversa_terminada=terminada)
    return render_template("home.html", passos=percurso.passos(estado))


@bp.get("/privacidade")
def privacy():
    return render_template("privacy.html")
