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
from ..catalogo import repository as catalogo_repository
from ..catalogo.repository import nomes_das_provas
from ..db import get_db
from ..percurso import services as percurso
from . import services
from .calculos import NOMES_CURTOS_DOS_EXAMES, NOMES_DOS_EXAMES

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
    """(código, nome) dos exames do formulário: um por prova, e nas Matemáticas o nome do exame
    (Matemática A, Matemática B, MACS; ver ``ACEITA`` em calculos.py)."""
    nomes = {**nomes_das_provas(current_app.config["CATALOGO_CSV"]), **NOMES_DOS_EXAMES}
    return sorted(nomes.items(), key=lambda p: p[1])


def _nomes_dos_exames() -> dict[str, str]:
    """Nomes para as notas e as combinações de exames do plano (Matemática B em vez de «Matemática»)."""
    return {**nomes_das_provas(current_app.config["CATALOGO_CSV"]), **NOMES_CURTOS_DOS_EXAMES}


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
    # Opções que saíram do catálogo (por exemplo, escondidas na gestão, US39): avisa em vez de as esconder.
    visiveis = {c.chave for c in cursos}
    da_dges = {c.chave: c for c in catalogo_repository.todos(current_app.config["CATALOGO_CSV"])}
    indisponiveis = [(chave, da_dges.get(chave)) for chave in plano.opcoes if chave not in visiveis]
    return render_template(
        "candidatura/plano.html",
        plano=plano,
        opcoes=lista,
        avisos=services.avisos(plano, lista),
        sugestoes=services.sugestoes(plano, cursos, area),
        area=area,
        curso_escolhido=curso_escolhido,
        indisponiveis=indisponiveis,
        partilha=services.codigo_de_partilha(db, g.user["id"]),
        combinacoes=services.exames_do_plano(plano, lista),
        plano_b=services.plano_b(plano, lista, cursos),
        nomes=nomes_das_provas(current_app.config["CATALOGO_CSV"]),
        nomes_exames=_nomes_dos_exames(),
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
    if not curso.concurso_nacional:          # ensino privado: candidatura na instituição (27/10)
        flash(texts.CANDIDATURA_FORA_DO_CONCURSO, "error")
        return _voltar()
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


# -- Partilhar o plano (23/10) --------------------------------------------------------------------

@bp.post("/partilhar")
@login_required
def partilhar():
    services.partilhar(get_db(), g.user["id"])
    flash(texts.PARTILHA_LIGADA, "ok")
    return redirect(url_for("candidatura.plano") + "#partilhar")


@bp.post("/deixar-de-partilhar")
@login_required
def deixar_de_partilhar():
    services.deixar_de_partilhar(get_db(), g.user["id"])
    flash(texts.PARTILHA_DESLIGADA, "ok")
    return redirect(url_for("candidatura.plano") + "#partilhar")


@bp.get("/p/<codigo>")
def partilhado(codigo: str):
    """O plano de alguém, só de leitura, para quem tem a ligação. Sem sessão; código errado = 404."""
    plano = services.plano_partilhado(get_db(), codigo, catalogo.cursos(current_app.config))
    if plano is None:
        abort(404)
    resposta = current_app.make_response(render_template(
        "candidatura/partilhado.html", partilhado=plano, nomes=nomes_das_provas(current_app.config["CATALOGO_CSV"]),
    ))
    resposta.headers["Cache-Control"] = "no-store"
    resposta.headers["Referrer-Policy"] = "no-referrer"     # o código não sai para outros sites
    return resposta
