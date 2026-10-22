"""Limite de pedidos ao LLM por aluno e por dia (revisão de 22/10).

O limite do fornecedor (por minuto e por dia) é partilhado por todos os utilizadores. Sem um
limite por conta, quem entrasse pelo túnel podia gastá-lo todo antes da demonstração.

``LimitarPedidosPorAluno`` embrulha o cliente do LLM (padrão Decorator, como
``ProtegerDadosPessoais`` em ``app/llm/decoradores.py``): conta só os pedidos que chegam mesmo
ao LLM, e os serviços da orientação não precisam de saber que o limite existe. Fica aqui, e não
em ``app/llm/``, porque é uma regra sobre alunos e não sobre fornecedores.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Callable, Sequence

from ..llm import ClienteLLM, ErroLLM, Mensagem
from . import repository


class LimiteDoAlunoAtingido(ErroLLM):
    """O aluno já fez o número máximo de pedidos ao LLM hoje. Não chega a haver pedido."""


def hoje_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


class LimitarPedidosPorAluno:
    def __init__(
        self,
        cliente: ClienteLLM,
        db: sqlite3.Connection,
        user_id: int,
        maximo_por_dia: int,
        *,
        hoje: Callable[[], str] | None = None,   # para os testes; por omissão, o dia de hoje em UTC
    ) -> None:
        self._cliente = cliente
        self._db = db
        self._user_id = user_id
        self._maximo = maximo_por_dia
        self._hoje = hoje
        self.nome = cliente.nome

    def conversar(self, instrucoes: str, mensagens: Sequence[Mensagem]) -> str:
        dia = (self._hoje or hoje_utc)()
        if self._maximo > 0 and repository.pedidos_no_dia(self._db, self._user_id, dia) >= self._maximo:
            raise LimiteDoAlunoAtingido(f"aluno {self._user_id}: {self._maximo} pedidos em {dia}")
        # Conta antes de pedir: um pedido que falha também gasta quota no fornecedor.
        repository.contar_pedido(self._db, self._user_id, dia)
        return self._cliente.conversar(instrucoes, mensagens)
