"""Interface que a aplicação usa para falar com um LLM (padrão Adapter, ver docs/geral/03).

O resto do código só conhece ``ClienteLLM`` e ``Mensagem``. Os pormenores de cada fornecedor
(endereço, formato do pedido, chave) ficam em ``adaptadores.py``.

Um LLM não se lembra de nada entre pedidos: cada chamada leva a conversa toda.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, Sequence

Papel = Literal["utilizador", "assistente"]


@dataclass(frozen=True)
class Mensagem:
    papel: Papel
    texto: str


class ErroLLM(Exception):
    """Falha ao obter resposta do LLM. A mensagem nunca inclui a chave."""


class LimiteAtingido(ErroLLM):
    """O fornecedor recusou por excesso de pedidos (HTTP 429): limite por minuto ou por dia."""


class LLMIndisponivel(ErroLLM):
    """Sem rede, fornecedor em baixo, chave em falta ou inválida, ou modelo inexistente."""


class RespostaInvalida(ErroLLM):
    """O LLM respondeu, mas não no formato pedido."""


class ClienteLLM(Protocol):
    nome: str     # para registos e para o comando de teste (ex.: «gemini/gemini-3.5-flash-lite»)

    def conversar(self, instrucoes: str, mensagens: Sequence[Mensagem]) -> str:
        """Devolve o texto da próxima resposta do assistente.

        ``instrucoes`` são as regras fixas (o «system prompt»); ``mensagens`` é a conversa até agora,
        a terminar numa mensagem do utilizador. A resposta pedida é JSON (ver orientacao/).
        """
        ...
