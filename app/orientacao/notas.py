"""O assistente que conhece as minhas notas (US37): o que o LLM recebe, só com autorização.

Funções puras, sem Flask nem base de dados. O LLM recebe só:
- os **nomes** dos exames nacionais que a pessoa fez (sem as notas de cada um);
- a média do secundário num **intervalo de 2 valores** («entre 14 e 16 valores»), nunca a exata (RNF12).

Antes de enviar o catálogo, ficam de fora os cursos a que falta uma prova de ingresso. Se assim
sobrarem poucos, vai o catálogo inteiro e os cursos com prova em falta são assinalados na página.
"""
from __future__ import annotations

import math
from typing import Mapping, Sequence

from ..candidatura.calculos import NOMES_CURTOS_DOS_EXAMES, Notas, provas_em_falta
from ..catalogo.repository import Curso

# Com menos cursos do que isto depois de tirar os que têm prova em falta, não se filtra.
MIN_CURSOS_FILTRADOS = 10
LARGURA_DO_INTERVALO = 2


def tem_o_que_partilhar(notas: Notas) -> bool:
    """Só se pede autorização a quem já indicou exames no plano de candidatura."""
    return bool(notas.exames)


def intervalo_da_media(media: float) -> tuple[int, int]:
    """15,2 -> (14, 16); 9,5 -> (10, 12); 19,6 -> (18, 20). Nunca a média exata."""
    inicio = LARGURA_DO_INTERVALO * math.floor(media / LARGURA_DO_INTERVALO)
    inicio = max(10, min(20 - LARGURA_DO_INTERVALO, inicio))
    return inicio, inicio + LARGURA_DO_INTERVALO


def nomes_dos_exames(notas: Notas, nomes_das_provas: Mapping[str, str]) -> list[str]:
    nomes = {**nomes_das_provas, **NOMES_CURTOS_DOS_EXAMES}
    return sorted(nomes.get(codigo, codigo) for codigo in notas.exames)


def contexto(notas: Notas, nomes_das_provas: Mapping[str, str]) -> str:
    """O texto que se junta às instruções do LLM. Vazio se a pessoa não tem exames indicados."""
    if not tem_o_que_partilhar(notas):
        return ""
    linhas = [
        "",
        "",
        "## O que a pessoa já fez",
        "",
        "A pessoa autorizou o OptaBem a dizer-lhe isto. Tem-no em conta e não sugiras cursos que peçam "
        "provas de ingresso que ela não fez. Não peças as notas exatas.",
        "",
        "- Exames nacionais feitos: " + ", ".join(nomes_dos_exames(notas, nomes_das_provas)) + ".",
    ]
    if notas.media is not None:
        inicio, fim = intervalo_da_media(notas.media)
        linhas.append(f"- Média do secundário: entre {inicio} e {fim} valores.")
    return "\n".join(linhas)


def cursos_para_enviar(catalogo: Sequence[Curso], notas: Notas) -> tuple[Curso, ...]:
    """O catálogo sem os cursos a que falta uma prova (ou inteiro, se sobrarem menos de ``MIN_CURSOS_FILTRADOS``)."""
    if not tem_o_que_partilhar(notas):
        return tuple(catalogo)
    possiveis = tuple(c for c in catalogo if not provas_em_falta(c, notas))
    return possiveis if len(possiveis) >= MIN_CURSOS_FILTRADOS else tuple(catalogo)


def em_falta_por_curso(cursos: Sequence[Curso], notas: Notas) -> dict[str, tuple[str, ...]]:
    """Para assinalar na página: chave do curso -> provas em falta (só os cursos com falta)."""
    if not tem_o_que_partilhar(notas):
        return {}
    return {c.chave: falta for c in cursos if (falta := provas_em_falta(c, notas))}
