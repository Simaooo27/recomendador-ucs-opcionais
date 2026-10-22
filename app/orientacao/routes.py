"""Página da conversa de orientação (US29) e dos cursos sugeridos no fim (US30): /orientacao.

As rotas só recebem o pedido e mostram a página; as regras estão em ``services.py``.
Abrir a página nunca chama o LLM: só os botões (POST) o fazem, para não gastar pedidos do
limite diário do fornecedor, que é partilhado por todos os utilizadores.
"""
from __future__ import annotations

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for

from .. import texts
from ..auth.sessions import login_required
from ..catalogo import services as catalogo
from ..db import get_db
from ..llm import ClienteLLM, ErroLLM, LimiteAtingido, criar_cliente_llm
from . import conversa, services
from .limite import LimitarPedidosPorAluno, LimiteDoAlunoAtingido

bp = Blueprint("orientacao", __name__, url_prefix="/orientacao")


def _cliente() -> ClienteLLM:
    """O cliente do LLM, criado na primeira utilização (os testes põem lá um LLM falso)."""
    if "llm" not in current_app.extensions:
        current_app.extensions["llm"] = criar_cliente_llm(current_app.config)
    return current_app.extensions["llm"]


def _com_o_llm(funcao, *argumentos) -> None:
    """Chama o serviço; se o LLM falhar, mostra uma mensagem clara (a conversa fica guardada).

    O cliente do LLM vai embrulhado no limite de pedidos por aluno e por dia (``limite.py``).
    """
    db = get_db()
    try:
        cliente = LimitarPedidosPorAluno(_cliente(), db, g.user["id"], current_app.config["ORIENTACAO_MAX_PEDIDOS_DIA"])
        funcao(db, g.user["id"], *argumentos, cliente, catalogo.cursos(current_app.config))
    except LimiteDoAlunoAtingido as erro:
        current_app.logger.info("Orientação: %s", erro)
        flash(texts.ORIENTACAO_ERRO_LIMITE_ALUNO, "error")
    except LimiteAtingido as erro:
        current_app.logger.warning("Orientação: %s", erro)
        flash(texts.ORIENTACAO_ERRO_LIMITE, "error")
    except (ErroLLM, RuntimeError) as erro:   # RuntimeError: LLM_BACKEND mal configurado
        current_app.logger.warning("Orientação: %s: %s", erro.__class__.__name__, erro)
        flash(texts.ORIENTACAO_ERRO_LLM, "error")


def _pagina(erro: str | None = None, resposta: str = "", estado_http: int = 200):
    estado = services.obter(get_db(), g.user["id"])
    return (
        render_template(
            "orientacao/conversa.html",
            estado=estado,
            sugestao=services.cursos_sugeridos(estado, catalogo.cursos(current_app.config)),
            min_cursos=conversa.MIN_CURSOS_SUGERIDOS,
            erro=erro,
            resposta=resposta,
            max_perguntas=conversa.LIMITE_PERGUNTAS,
            max_caracteres=conversa.MAX_CARACTERES_RESPOSTA,
        ),
        estado_http,
    )


def _voltar():
    return redirect(url_for("orientacao.pagina", _anchor="resposta"))


@bp.get("/")
@login_required
def pagina():
    return _pagina()


@bp.post("/comecar")
@login_required
def comecar():
    _com_o_llm(services.comecar)
    return _voltar()


@bp.post("/responder")
@login_required
def responder():
    texto = request.form.get("resposta", "")
    try:
        services.validar_resposta(texto)
    except services.RespostaVazia:
        return _pagina(texts.ORIENTACAO_ERRO_VAZIA, texto, 400)
    except services.RespostaLonga:
        return _pagina(texts.ORIENTACAO_ERRO_LONGA.format(maximo=conversa.MAX_CARACTERES_RESPOSTA), texto, 400)
    _com_o_llm(services.responder, texto)
    return _voltar()


@bp.post("/tentar-de-novo")
@login_required
def tentar_de_novo():
    _com_o_llm(services.continuar)
    return _voltar()


@bp.post("/sugerir")
@login_required
def sugerir():
    """«Ver sugestões já» (US30)."""
    _com_o_llm(services.pedir_sugestao)
    return redirect(url_for("orientacao.pagina", _anchor="sugestoes"))


@bp.post("/continuar")
@login_required
def continuar_conversa():
    """Menos de 2 cursos sugeridos: voltar à conversa para dar mais pistas (US30). Não chama o LLM."""
    services.continuar_conversa(get_db(), g.user["id"])
    return _voltar()


@bp.post("/recomecar")
@login_required
def recomecar():
    services.recomecar(get_db(), g.user["id"])
    return redirect(url_for("orientacao.pagina"))
