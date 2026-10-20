"""Rotas do catálogo: a página /cursos/ e a pesquisa em JSON usada pela página de apresentação.

Os filtros, a ficha de cada curso e a comparação são a US05.
"""
from __future__ import annotations

from flask import current_app, jsonify, render_template, request

from . import bp, services


@bp.get("/")
def lista():
    """Pesquisa no catálogo numa página própria, com ou sem sessão iniciada.

    É para aqui que leva «Procurar no catálogo», quando a conversa de orientação acaba com
    menos de 2 cursos sugeridos (US30). A página de apresentação (/) só a vê quem não tem sessão.
    """
    termo = request.args.get("q", "")[:80]
    return render_template("catalogo/lista.html", termo=termo, resultado=services.pesquisar(current_app.config, termo))


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
            }
            for c in resultado.cursos
        ],
    )
