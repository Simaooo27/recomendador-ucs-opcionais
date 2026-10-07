"""Páginas gerais."""
from flask import Blueprint, g, redirect, render_template, url_for

from .auth.sessions import login_required

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    """Com sessão iniciada vai para a área do aluno; sem sessão, para o início de sessão."""
    return redirect(url_for("main.home" if g.user is not None else "auth.login_form"))


@bp.get("/inicio")
@login_required
def home():
    return render_template("home.html")


@bp.get("/privacidade")
def privacy():
    return render_template("privacy.html")
