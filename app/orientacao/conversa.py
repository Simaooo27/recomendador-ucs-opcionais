"""Conversa de orientação conduzida pelo LLM (spike para a US29 e a US30).

Em cada passo, a aplicação envia ao LLM as instruções (``instrucoes.md`` com o catálogo) e a
conversa até agora; o LLM responde com a próxima pergunta ou com 2 a 3 cursos sugeridos.

Garantias que não dependem do LLM:

- RNF12: estas funções não recebem a conta do utilizador, só o texto da conversa; e o cliente
  criado pela fábrica apaga emails e números longos antes de enviar (``llm/decoradores.py``).
- RN09: ``validar_contra_catalogo`` descarta qualquer curso que não exista no catálogo, seja
  inventado pelo LLM ou pedido pelo utilizador («recomende-me Medicina em Harvard»).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from string import Template
from typing import Sequence

from ..catalogo.repository import Curso
from ..llm import ClienteLLM, Mensagem, RespostaInvalida

LIMITE_PERGUNTAS = 6            # depois disto, o LLM tem de sugerir (poupa pedidos ao plano gratuito)
MIN_CURSOS_SUGERIDOS = 2        # RF37: 2 a 3 cursos; com menos, a página propõe continuar (US30)
MAX_CURSOS_SUGERIDOS = 3
MAX_CARACTERES_RESPOSTA = 500   # cada resposta do utilizador (protege o limite de tokens)
MAX_CARACTERES_EXPLICACAO = 400
ABERTURA = "Olá! Quero ajuda para escolher um curso."
PEDIDO_DE_SUGESTAO = (
    "\n\n## Agora\n\nJá tem informação suficiente: responda agora com o formato «sugestao», "
    "sem fazer mais perguntas."
)

_INSTRUCOES = Path(__file__).with_name("instrucoes.md")


@dataclass(frozen=True)
class Pergunta:
    texto: str


@dataclass(frozen=True)
class CursoSugerido:
    curso: Curso
    explicacao: str


@dataclass(frozen=True)
class Sugestao:
    texto: str
    cursos: tuple[CursoSugerido, ...]
    descartados: tuple[str, ...]   # identificadores devolvidos pelo LLM que não estão no catálogo


def linha_do_catalogo(curso: Curso) -> str:
    return " | ".join(
        (
            curso.chave,
            curso.curso,
            f"{curso.instituicao} ({curso.unidade_organica})" if curso.unidade_organica else curso.instituicao,
            curso.localidade,
            curso.tipo_ensino,
            curso.area,
            curso.ultimo_colocado or "sem dados",
            curso.descricao,
            curso.saidas,
        )
    )


@lru_cache(maxsize=8)
def _instrucoes_em_cache(catalogo: tuple[Curso, ...]) -> str:
    modelo = Template(_INSTRUCOES.read_text(encoding="utf-8"))
    return modelo.substitute(
        max_perguntas=LIMITE_PERGUNTAS, catalogo="\n".join(linha_do_catalogo(c) for c in catalogo)
    )


def instrucoes(catalogo: Sequence[Curso]) -> str:
    return _instrucoes_em_cache(tuple(catalogo))


def interpretar(texto: str) -> dict:
    """Lê o JSON devolvido pelo LLM (aceita-o dentro de um bloco ```json)."""
    limpo = texto.strip()
    if limpo.startswith("```"):
        limpo = limpo.strip("`").removeprefix("json").strip()
    try:
        dados = json.loads(limpo)
    except json.JSONDecodeError:
        raise RespostaInvalida("O LLM não respondeu em JSON.") from None
    if not isinstance(dados, dict) or dados.get("tipo") not in ("pergunta", "sugestao"):
        raise RespostaInvalida("O JSON do LLM não tem «tipo» igual a «pergunta» ou «sugestao».")
    return dados


def validar_contra_catalogo(dados: dict, catalogo: Sequence[Curso]) -> Sugestao:
    """RN09: só ficam cursos do catálogo, sem repetidos, no máximo ``MAX_CURSOS_SUGERIDOS``."""
    por_chave = {curso.chave: curso for curso in catalogo}
    aceites: list[CursoSugerido] = []
    descartados: list[str] = []
    for item in dados.get("cursos") or []:
        if not isinstance(item, dict):
            continue
        chave = str(item.get("id", "")).strip()
        curso = por_chave.get(chave)
        if curso is None:
            descartados.append(chave or "(sem identificador)")
        elif all(sugerido.curso.chave != chave for sugerido in aceites) and len(aceites) < MAX_CURSOS_SUGERIDOS:
            explicacao = " ".join(str(item.get("explicacao", "")).split())[:MAX_CARACTERES_EXPLICACAO]
            aceites.append(CursoSugerido(curso, explicacao))
    return Sugestao(str(dados.get("texto", "")).strip(), tuple(aceites), tuple(descartados))


def proximo_passo(
    cliente: ClienteLLM,
    catalogo: Sequence[Curso],
    conversa: Sequence[Mensagem],
    *,
    forcar_sugestao: bool = False,
) -> Pergunta | Sugestao:
    """Pede ao LLM o passo seguinte da conversa: uma pergunta ou a sugestão de cursos.

    ``conversa`` são as mensagens trocadas até agora (vazia no início). O chamador acrescenta a
    resposta do LLM à conversa como mensagem do «assistente» antes do passo seguinte.

    Depois de ``LIMITE_PERGUNTAS`` respostas (ou com ``forcar_sugestao``), só aceita a sugestão:
    se o LLM fizer outra pergunta, levanta ``RespostaInvalida``.
    """
    mensagens = [Mensagem("utilizador", ABERTURA)] + [
        Mensagem(m.papel, m.texto[:MAX_CARACTERES_RESPOSTA] if m.papel == "utilizador" else m.texto)
        for m in conversa
    ]
    respostas_do_utilizador = sum(1 for m in conversa if m.papel == "utilizador")
    texto_instrucoes = instrucoes(catalogo)
    exigir_sugestao = forcar_sugestao or respostas_do_utilizador >= LIMITE_PERGUNTAS
    if exigir_sugestao:
        texto_instrucoes += PEDIDO_DE_SUGESTAO
    dados = interpretar(cliente.conversar(texto_instrucoes, mensagens))
    if dados["tipo"] == "pergunta":
        if exigir_sugestao:
            # O limite não pode depender de o LLM obedecer: uma pergunta a mais é uma resposta
            # fora do formato pedido (a página mostra «Tentar de novo» e não gasta mais perguntas).
            raise RespostaInvalida("O LLM fez outra pergunta depois de lhe ter sido pedida a sugestão.")
        return Pergunta(" ".join(str(dados.get("texto", "")).split()))
    return validar_contra_catalogo(dados, catalogo)
