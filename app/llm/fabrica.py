"""Escolhe o LLM pela configuração (padrão Factory, como ``create_mailer`` em app/mailer.py).

| LLM_BACKEND | Fornecedor                              | Chave no .env   |
|-------------|-----------------------------------------|-----------------|
| falso       | respostas fixas, sem rede (por omissão) | —               |
| gemini      | Google Gemini, plano gratuito           | GEMINI_API_KEY  |
| groq        | Groq, plano gratuito (reserva)          | GROQ_API_KEY    |

``LLM_MODELO`` muda o modelo; vazio usa o de ``MODELOS_POR_OMISSAO``.
Qualquer que seja o fornecedor, o cliente vem sempre embrulhado em ``ProtegerDadosPessoais`` (RNF12).
"""
from __future__ import annotations

from typing import Mapping

from .adaptadores import AdaptadorGemini, AdaptadorGroq, LLMFalso
from .cliente import ClienteLLM
from .decoradores import ProtegerDadosPessoais

# Escolhidos pelos limites do plano gratuito (ver docs/geral/05-spike-llm.md):
# numa medição independente (não oficial), o Gemini Flash dava cerca de 20 pedidos por dia
# e o Flash-Lite cerca de 500. Cada conta vê os seus em https://aistudio.google.com/rate-limit.
MODELOS_POR_OMISSAO = {
    "gemini": "gemini-3.5-flash-lite",
    "groq": "openai/gpt-oss-120b",
}


def criar_cliente_llm(config: Mapping) -> ClienteLLM:
    backend = (config.get("LLM_BACKEND") or "falso").strip().lower()
    modelo = (config.get("LLM_MODELO") or "").strip() or MODELOS_POR_OMISSAO.get(backend, "")
    timeout = float(config.get("LLM_TIMEOUT", 15))
    if backend == "falso":
        cliente: ClienteLLM = LLMFalso()
    elif backend == "gemini":
        cliente = AdaptadorGemini(chave=config.get("GEMINI_API_KEY", ""), modelo=modelo, timeout=timeout)
    elif backend == "groq":
        cliente = AdaptadorGroq(chave=config.get("GROQ_API_KEY", ""), modelo=modelo, timeout=timeout)
    else:
        raise RuntimeError(f"LLM_BACKEND desconhecido: {backend!r} (use 'falso', 'gemini' ou 'groq').")
    return ProtegerDadosPessoais(cliente)
