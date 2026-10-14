"""Ligação a um LLM atrás de uma interface própria (US30; ver docs/geral/03, secções 4.2 a 4.4).

Fora deste pacote, o código só importa daqui: ``criar_cliente_llm``, ``ClienteLLM``, ``Mensagem``
e os erros. Nenhum outro ficheiro conhece o fornecedor.
"""
from .cliente import ClienteLLM, ErroLLM, LimiteAtingido, LLMIndisponivel, Mensagem, RespostaInvalida
from .fabrica import criar_cliente_llm

__all__ = [
    "ClienteLLM",
    "ErroLLM",
    "LimiteAtingido",
    "LLMIndisponivel",
    "Mensagem",
    "RespostaInvalida",
    "criar_cliente_llm",
]
