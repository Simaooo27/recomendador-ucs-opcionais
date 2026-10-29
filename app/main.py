"""Páginas gerais."""
from datetime import date

from flask import Blueprint, current_app, g, redirect, render_template, request, url_for

from . import percurso
from .catalogo import services as catalogo
from .auth.sessions import login_required
from .candidatura import calendario
from .db import get_db
from .orientacao import services as orientacao_services
from .percurso import services as percurso_services

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
    curso = percurso_services.curso_atual(get_db(), g.user["id"])
    estado = percurso.estado_do_utilizador(g.user, conversa_terminada=terminada, tem_curso=curso is not None)
    # O passo atual mostra o próximo prazo do concurso nacional (US38).
    prazo = calendario.proximo_prazo(calendario.ler(current_app.config["CALENDARIO_CSV"]), date.today())
    return render_template(
        "home.html", passos=percurso.passos(estado, curso), prazo=calendario.frase_do_prazo(prazo),
        pagina_calendario=calendario.PAGINA_DGES,
    )


@bp.get("/privacidade")
def privacy():
    return render_template("privacy.html")
