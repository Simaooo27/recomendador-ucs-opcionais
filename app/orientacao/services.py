"""Regras da conversa de orientação (US29): começar, responder, tentar de novo e recomeçar.

A conversa fica guardada no servidor, uma por aluno. Estas funções nunca recebem nem enviam o
email ou o nome do aluno: só o identificador interno, usado para guardar a conversa (RNF12).
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from ..catalogo.repository import Curso
from ..llm import ClienteLLM, Mensagem
from ..llm.decoradores import remover_dados_pessoais
from . import conversa, repository


class RespostaVazia(ValueError):
    pass


class RespostaLonga(ValueError):
    pass


@dataclass(frozen=True)
class EstadoConversa:
    mensagens: tuple[Mensagem, ...]
    sugestao: dict | None          # a sugestão final, em JSON (mostrada pela US30)

    @property
    def comecada(self) -> bool:
        return bool(self.mensagens)

    @property
    def terminada(self) -> bool:
        return self.sugestao is not None

    @property
    def a_espera_do_assistente(self) -> bool:
        """A última mensagem é do aluno: o LLM falhou e é preciso tentar de novo."""
        return self.comecada and not self.terminada and self.mensagens[-1].papel == "utilizador"

    @property
    def perguntas_feitas(self) -> int:
        return sum(1 for m in self.mensagens if m.papel == "assistente")


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def obter(db: sqlite3.Connection, user_id: int) -> EstadoConversa:
    linha = repository.obter(db, user_id)
    if linha is None:
        return EstadoConversa((), None)
    mensagens = tuple(Mensagem(m["papel"], m["texto"]) for m in json.loads(linha["mensagens"]))
    return EstadoConversa(mensagens, json.loads(linha["sugestao"]) if linha["sugestao"] else None)


def _guardar(db: sqlite3.Connection, user_id: int, estado: EstadoConversa) -> None:
    mensagens = json.dumps([{"papel": m.papel, "texto": m.texto} for m in estado.mensagens], ensure_ascii=False)
    sugestao = json.dumps(estado.sugestao, ensure_ascii=False) if estado.sugestao is not None else None
    repository.guardar(db, user_id, mensagens, sugestao, _agora())


def _sugestao_em_json(sugestao: conversa.Sugestao) -> dict:
    return {
        "texto": sugestao.texto,
        "cursos": [{"id": s.curso.chave, "explicacao": s.explicacao} for s in sugestao.cursos],
        "descartados": list(sugestao.descartados),
    }


def _pedir_ao_llm(
    db: sqlite3.Connection, user_id: int, estado: EstadoConversa, cliente: ClienteLLM, catalogo: Sequence[Curso]
) -> EstadoConversa:
    """Pede o próximo passo ao LLM e guarda-o. Se o LLM falhar, o erro sobe e a conversa fica como estava."""
    passo = conversa.proximo_passo(cliente, catalogo, estado.mensagens)
    if isinstance(passo, conversa.Pergunta):
        novo = EstadoConversa(estado.mensagens + (Mensagem("assistente", passo.texto),), None)
    else:
        texto = passo.texto or "Já tenho informação suficiente para lhe sugerir cursos."
        novo = EstadoConversa(estado.mensagens + (Mensagem("assistente", texto),), _sugestao_em_json(passo))
    _guardar(db, user_id, novo)
    return novo


def comecar(db: sqlite3.Connection, user_id: int, cliente: ClienteLLM, catalogo: Sequence[Curso]) -> EstadoConversa:
    """Primeira pergunta do assistente. Se a conversa já começou, não faz nada."""
    estado = obter(db, user_id)
    if estado.comecada:
        return estado
    return _pedir_ao_llm(db, user_id, estado, cliente, catalogo)


def validar_resposta(texto: str) -> str:
    texto = " ".join((texto or "").split())
    if not texto:
        raise RespostaVazia()
    if len(texto) > conversa.MAX_CARACTERES_RESPOSTA:
        raise RespostaLonga()
    return texto


def responder(
    db: sqlite3.Connection, user_id: int, texto: str, cliente: ClienteLLM, catalogo: Sequence[Curso]
) -> EstadoConversa:
    """Guarda a resposta do aluno (sem dados pessoais) e pede a próxima pergunta ao LLM.

    A resposta é guardada antes de chamar o LLM: se ele falhar, a conversa não se perde e o
    aluno pode tentar de novo (``continuar``).
    """
    estado = obter(db, user_id)
    if not estado.comecada or estado.terminada or estado.a_espera_do_assistente:
        return estado
    limpo = remover_dados_pessoais(validar_resposta(texto))
    estado = EstadoConversa(estado.mensagens + (Mensagem("utilizador", limpo),), None)
    _guardar(db, user_id, estado)
    return _pedir_ao_llm(db, user_id, estado, cliente, catalogo)


def continuar(db: sqlite3.Connection, user_id: int, cliente: ClienteLLM, catalogo: Sequence[Curso]) -> EstadoConversa:
    """Tenta de novo depois de o LLM ter falhado."""
    estado = obter(db, user_id)
    if not estado.a_espera_do_assistente:
        return estado
    return _pedir_ao_llm(db, user_id, estado, cliente, catalogo)


def recomecar(db: sqlite3.Connection, user_id: int) -> None:
    repository.apagar(db, user_id)


def tem_sugestao(db: sqlite3.Connection, user_id: int) -> bool:
    return obter(db, user_id).terminada
