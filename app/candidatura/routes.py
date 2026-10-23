"""Páginas do plano de candidatura (/candidatura). Só com sessão iniciada.

- ``GET /candidatura/``: as opções, por ordem, com a nota de candidatura e os avisos;
- ``GET|POST /candidatura/notas``: a média do secundário e os exames nacionais;
- ``POST /candidatura/juntar/<chave>``, ``retirar``, ``subir``, ``descer``: mudar a lista.

Os botões são formulários (POST com CSRF): funcionam sem JavaScript. As regras estão em ``services.py``.
"""
from __future__ import annotations

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for

from .. import texts
from ..auth.sessions import login_required
from ..catalogo import services as catalogo
from ..catalogo.repository import nomes_das_provas
from ..db import get_db
from ..percurso import services as percurso
from . import services
from .calculos import EQUIVALENTES

bp = Blueprint("candidatura", __name__, url_prefix="/candidatura")


@bp.app_template_filter("pontos")
def _pontos(valor, sinal: bool = False) -> str:
    """146.0 -> «146,0»; com ``sinal``: 7.7 -> «+7,7» e -1.8 -> «−1,8» (também usado na ficha)."""
    if valor is None:
        return ""
    texto = f"{abs(valor) if sinal else valor:.1f}".replace(".", ",")
    if sinal:
        return ("+" if valor >= 0 else "−") + texto
    return texto


def _provas_do_formulario() -> list[tuple[str, str]]:
    """(código, nome) das provas que aparecem no formulário. As equivalentes aparecem uma vez."""
    nomes = nomes_das_provas(current_app.config["CATALOGO_CSV"])
    escondidas = set(EQUIVALENTES)          # «16 Matemática» fica com a nota de «19 Matemática A»
    return [(codigo, nome) for codigo, nome in sorted(nomes.items(), key=lambda p: p[1]) if codigo not in escondidas]


@bp.get("/")
@login_required
def plano():
    db = get_db()
    plano = services.obter(db, g.user["id"])
    cursos = catalogo.cursos(current_app.config)
    # Quem já escolheu um curso (US31) e ainda não tem opções vê um botão para o pôr em 1.º lugar.
    atual = percurso.curso_atual(db, g.user["id"]) if not plano.opcoes else None
    curso_escolhido = catalogo.por_chave(current_app.config, atual.curso_chave) if atual else None
    lista = services.opcoes(plano, cursos)
    area = lista[0].curso.area if lista else ""
    return render_template(
        "candidatura/plano.html",
        plano=plano,
        opcoes=lista,
        avisos=services.avisos(plano, lista),
        sugestoes=services.sugestoes(plano, cursos, area),
        area=area,
        curso_escolhido=curso_escolhido,
        nomes=nomes_das_provas(current_app.config["CATALOGO_CSV"]),
        maximo=services.MAX_OPCOES,
    )


@bp.route("/notas", methods=["GET", "POST"])
@login_required
def notas():
    provas = _provas_do_formulario()
    if request.method == "POST":
        lidas, erros = services.ler_notas(request.form, [codigo for codigo, _ in provas])
        if not erros:
            services.guardar_notas(get_db(), g.user["id"], lidas)
            flash(texts.CANDIDATURA_NOTAS_GUARDADAS, "ok")
            return redirect(url_for("candidatura.plano"))
        return render_template("candidatura/notas.html", provas=provas, valores=request.form, erros=erros), 422
    plano = services.obter(get_db(), g.user["id"])
    valores = {}
    if plano.notas.media is not None:
        valores["media"] = f"{plano.notas.media:g}".replace(".", ",")
    for codigo, valor in plano.notas.exames.items():
        valores[f"exame_{codigo}"] = f"{valor:g}".replace(".", ",")
    return render_template("candidatura/notas.html", provas=provas, valores=valores, erros={})


def _curso_ou_404(chave: str):
    curso = catalogo.por_chave(current_app.config, chave)
    if curso is None:
        abort(404)
    return curso


def _voltar():
    """Volta à página de onde veio o botão (a ficha do curso ou o plano)."""
    destino = request.form.get("voltar", "")
    return redirect(destino if destino.startswith("/") and not destino.startswith("//") else url_for("candidatura.plano"))


@bp.post("/juntar/<chave>")
@login_required
def juntar(chave: str):
    curso = _curso_ou_404(chave)
    try:
        if services.juntar(get_db(), g.user["id"], chave):
            flash(texts.CANDIDATURA_JUNTADO.format(curso=curso.curso), "ok")
    except services.PlanoCheio:
        flash(texts.CANDIDATURA_CHEIO.format(maximo=services.MAX_OPCOES), "error")
    return _voltar()


@bp.post("/retirar/<chave>")
@login_required
def retirar(chave: str):
    services.retirar(get_db(), g.user["id"], chave)
    return _voltar()


@bp.post("/subir/<chave>")
@login_required
def subir(chave: str):
    services.mover(get_db(), g.user["id"], chave, -1)
    return _voltar()


@bp.post("/descer/<chave>")
@login_required
def descer(chave: str):
    services.mover(get_db(), g.user["id"], chave, +1)
    return _voltar()
