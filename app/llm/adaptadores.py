"""Adaptadores de LLM (padrão Adapter): cada um traduz ``ClienteLLM`` para um fornecedor.

- ``LLMFalso``: respostas fixas, sem rede. É o que os testes usam (RNF06).
- ``AdaptadorGemini``: Google Gemini (API REST ``generateContent``).
- ``AdaptadorGroq``: Groq (API compatível com a da OpenAI). Reserva para quando o Gemini falhar.

Os pedidos são feitos com ``urllib`` (biblioteca padrão), sem SDK de nenhum fornecedor: menos uma
dependência e o pedido fica visível neste ficheiro. A chave vai sempre num cabeçalho, nunca no
endereço, para não aparecer em registos; e é apagada de qualquer mensagem de erro.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Callable, Sequence

from .cliente import ErroLLM, LimiteAtingido, LLMIndisponivel, Mensagem, RespostaInvalida

# transporte(url, cabeçalhos, corpo, timeout) -> resposta em JSON. Os testes trocam-no por um falso.
Transporte = Callable[[str, dict, dict, float], dict]


class ErroHTTP(Exception):
    def __init__(self, codigo: int, corpo: str) -> None:
        super().__init__(codigo)
        self.codigo, self.corpo = codigo, corpo


def transporte_urllib(url: str, cabecalhos: dict, corpo: dict, timeout: float) -> dict:
    pedido = urllib.request.Request(
        url, data=json.dumps(corpo).encode("utf-8"), headers={"Content-Type": "application/json", **cabecalhos}
    )
    try:
        with urllib.request.urlopen(pedido, timeout=timeout) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        raise ErroHTTP(erro.code, erro.read().decode("utf-8", "replace")) from None
    except (urllib.error.URLError, TimeoutError, OSError) as erro:
        raise LLMIndisponivel(f"Sem ligação ao fornecedor ({erro.__class__.__name__}).") from None
    except json.JSONDecodeError:
        raise RespostaInvalida("O fornecedor devolveu algo que não é JSON.") from None


def _mensagem_do_fornecedor(corpo: str) -> str:
    try:
        dados = json.loads(corpo)
        erro = dados.get("error", dados)
        texto = erro.get("message", "") if isinstance(erro, dict) else str(erro)
    except (json.JSONDecodeError, AttributeError):
        texto = corpo
    return " ".join(texto.split())[:300]


def _traduzir_erro(erro: ErroHTTP, fornecedor: str, modelo: str, chave: str) -> ErroLLM:
    detalhe = _mensagem_do_fornecedor(erro.corpo)
    if chave:
        detalhe = detalhe.replace(chave, "***")
    if erro.codigo == 429:
        return LimiteAtingido(f"{fornecedor}: limite de pedidos atingido (por minuto ou por dia). {detalhe}")
    if erro.codigo in (401, 403):
        return LLMIndisponivel(f"{fornecedor}: chave recusada ({erro.codigo}). {detalhe}")
    if erro.codigo == 404:
        return LLMIndisponivel(f"{fornecedor}: o modelo {modelo!r} não existe ou não está disponível. {detalhe}")
    return LLMIndisponivel(f"{fornecedor}: erro {erro.codigo}. {detalhe}")


class LLMFalso:
    """Devolve as respostas dadas, por ordem (repete a última). Guarda o que lhe foi enviado."""

    nome = "falso"

    def __init__(self, respostas: Sequence[str] | None = None) -> None:
        self._respostas = list(respostas or ['{"tipo": "pergunta", "texto": "Resposta simulada (LLM_BACKEND=falso)."}'])
        self.pedidos: list[tuple[str, tuple[Mensagem, ...]]] = []

    def conversar(self, instrucoes: str, mensagens: Sequence[Mensagem]) -> str:
        self.pedidos.append((instrucoes, tuple(mensagens)))
        indice = min(len(self.pedidos) - 1, len(self._respostas) - 1)
        return self._respostas[indice]


class AdaptadorGemini:
    ENDERECO = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

    def __init__(self, *, chave: str, modelo: str, timeout: float = 30, transporte: Transporte = transporte_urllib) -> None:
        if not chave:
            raise LLMIndisponivel("LLM_BACKEND=gemini exige GEMINI_API_KEY no .env.")
        self._chave, self.modelo, self._timeout, self._transporte = chave, modelo, timeout, transporte
        self.nome = f"gemini/{modelo}"

    def conversar(self, instrucoes: str, mensagens: Sequence[Mensagem]) -> str:
        corpo = {
            "systemInstruction": {"parts": [{"text": instrucoes}]},
            "contents": [
                {"role": "user" if m.papel == "utilizador" else "model", "parts": [{"text": m.texto}]} for m in mensagens
            ],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7},
        }
        try:
            dados = self._transporte(
                self.ENDERECO.format(modelo=self.modelo), {"x-goog-api-key": self._chave}, corpo, self._timeout
            )
        except ErroHTTP as erro:
            raise _traduzir_erro(erro, "Gemini", self.modelo, self._chave) from None
        candidatos = dados.get("candidates") or []
        if not candidatos:
            motivo = (dados.get("promptFeedback") or {}).get("blockReason", "sem candidatos")
            raise RespostaInvalida(f"Gemini não respondeu ({motivo}).")
        partes = (candidatos[0].get("content") or {}).get("parts") or []
        texto = "".join(p.get("text", "") for p in partes if not p.get("thought"))
        if not texto.strip():
            raise RespostaInvalida(f"Gemini devolveu uma resposta vazia ({candidatos[0].get('finishReason')}).")
        return texto


class AdaptadorGroq:
    ENDERECO = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, *, chave: str, modelo: str, timeout: float = 30, transporte: Transporte = transporte_urllib) -> None:
        if not chave:
            raise LLMIndisponivel("LLM_BACKEND=groq exige GROQ_API_KEY no .env.")
        self._chave, self.modelo, self._timeout, self._transporte = chave, modelo, timeout, transporte
        self.nome = f"groq/{modelo}"

    def conversar(self, instrucoes: str, mensagens: Sequence[Mensagem]) -> str:
        corpo = {
            "model": self.modelo,
            "messages": [{"role": "system", "content": instrucoes}]
            + [{"role": "user" if m.papel == "utilizador" else "assistant", "content": m.texto} for m in mensagens],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
        }
        try:
            dados = self._transporte(self.ENDERECO, {"Authorization": f"Bearer {self._chave}"}, corpo, self._timeout)
        except ErroHTTP as erro:
            raise _traduzir_erro(erro, "Groq", self.modelo, self._chave) from None
        try:
            texto = dados["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            raise RespostaInvalida("Groq devolveu uma resposta sem «choices».") from None
        if not texto.strip():
            raise RespostaInvalida("Groq devolveu uma resposta vazia.")
        return texto
