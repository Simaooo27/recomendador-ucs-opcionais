"""Páginas gerais."""
from flask import Blueprint, g, redirect, render_template, url_for

from . import percurso
from .auth.sessions import login_required

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    """Com sessão iniciada vai para a área de cada perfil; sem sessão, mostra a apresentação."""
    if g.user is not None:
        return redirect(url_for("main.home"))
    if g.get("admin") is not None:
        return redirect(url_for("gestao.dashboard"))
    return render_template("landing.html")


@bp.get("/inicio")
@login_required
def home():
    estado = percurso.estado_do_utilizador(g.user)
    return render_template("home.html", passos=percurso.passos(estado))


@bp.get("/privacidade")
def privacy():
    return render_template("privacy.html")
