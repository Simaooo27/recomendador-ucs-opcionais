"""Rotas do catálogo. Por agora só a pesquisa usada pela página de apresentação."""
from __future__ import annotations

from flask import current_app, jsonify, request

from . import bp, services


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
