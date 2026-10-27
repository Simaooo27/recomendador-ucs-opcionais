"""Rotas do catálogo (US05): a lista com filtros (/cursos/), a ficha de cada curso, a comparação
de até 3 cursos e a pesquisa em JSON usada pela página de apresentação.

Tudo funciona sem sessão iniciada e sem JavaScript: os filtros e os cursos a comparar vão no
endereço (?area=…&c=…). As regras estão em ``services.py``.
"""
from __future__ import annotations

from flask import abort, current_app, g, jsonify, render_template, request, url_for

from . import bp, services
from .repository import nomes_das_provas


@bp.get("/")
def lista():
    """Pesquisa no catálogo numa página própria, com ou sem sessão iniciada.

    É para aqui que leva «Procurar no catálogo», quando a conversa de orientação acaba com
    menos de 2 cursos sugeridos (US30). A página de apresentação (/) só a vê quem não tem sessão.
    """
    filtros = services.ler_filtros(request.args, current_app.config)
    pagina = services.paginar(services.filtrar(current_app.config, filtros), request.args.get("p"))
    return render_template(
        "catalogo/lista.html",
        filtros=filtros,
        opcoes=services.opcoes(current_app.config),
        cursos=pagina.cursos,
        pagina=pagina,
        total=len(services.cursos(current_app.config)),
        max_comparar=services.MAX_COMPARAR,
    )


@bp.get("/comparar")
def comparar():
    """Comparação lado a lado de 2 ou 3 cursos (/cursos/comparar?c=…&c=…)."""
    comparacao = services.comparar(current_app.config, request.args.getlist("c")[:20])
    return render_template(
        "catalogo/comparar.html",
        comparacao=comparacao,
        minimo=services.MIN_COMPARAR,
        maximo=services.MAX_COMPARAR,
    ), (200 if comparacao.suficiente else 400)


@bp.get("/<chave>")
def ficha(chave: str):
    """Ficha completa de um curso. Um identificador que não existe dá «página não encontrada»."""
    curso = services.por_chave(current_app.config, chave)
    if curso is None:
        abort(404)
    simulacao, no_plano, necessidade = None, False, None
    if g.user is not None:   # plano de candidatura (23/10): a nota do aluno neste curso
        from ..candidatura import services as candidatura
        from ..candidatura.calculos import nota_necessaria, simular
        from ..db import get_db

        plano = candidatura.obter(get_db(), g.user["id"])
        simulacao, no_plano = simular(curso, plano.notas), chave in plano.opcoes
        necessidade = nota_necessaria(curso, plano.notas)
    return render_template(
        "catalogo/ficha.html",
        curso=curso,
        nomes_provas=nomes_das_provas(current_app.config["CATALOGO_CSV"]),
        simulacao=simulacao,
        no_plano=no_plano,
        necessidade=necessidade,
    )


@bp.get("/pesquisa")
def pesquisa():
    """Resultados em JSON para a pesquisa enquanto se escreve (app/static/app.js)."""
    termo = request.args.get("q", "")[:80]
    resultado = services.pesquisar(current_app.config, termo)
    return jsonify(
        termo=termo,
        total=resultado.total,
        amostra=resultado.amostra,
        cursos=[
            {
                "curso": c.curso,
                "instituicao": c.instituicao,
                "unidade": c.unidade_organica,
                "localidade": c.localidade,
                "area": c.area,
                "vagas": c.vagas,
                "ultimo_colocado": c.ultimo_colocado,
                "fonte": c.fonte,
                "chave": c.chave,
                "ficha": url_for("catalogo.ficha", chave=c.chave),
            }
            for c in resultado.cursos
        ],
    )
