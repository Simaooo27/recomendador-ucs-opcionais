"""Catálogo de cursos: pesquisa (página de apresentação), filtros, ficha e comparação (US05).

Tudo funciona sem sessão iniciada (RF34). Os cursos vêm de ``repository.todos``.
"""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Mapping

from . import repository
from .repository import Curso


def _normalizar(texto: str) -> str:
    """Minúsculas e sem acentos, para «informatica» encontrar «Informática»."""
    decomposto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def cursos(config: Mapping) -> tuple[Curso, ...]:
    return repository.todos(config["CATALOGO_CSV"])


@dataclass(frozen=True)
class Resultado:
    cursos: list[Curso]   # os que se mostram (no máximo ``limite``)
    total: int            # quantos cursos correspondem ao termo
    amostra: bool         # True quando não havia termo e se mostra uma amostra


def pesquisar(config: Mapping, termo: str, limite: int = 60) -> Resultado:
    """Cursos em que todas as palavras do termo aparecem no nome, instituição, localidade ou área.

    Sem termo, devolve uma amostra variada (um curso de cada instituição, por ordem de vagas).
    """
    todos = cursos(config)
    palavras = _normalizar(termo or "").split()
    if not palavras:
        vistos, amostra = set(), []
        for curso in sorted(todos, key=lambda c: -(c.vagas or 0)):
            if curso.instituicao not in vistos:
                vistos.add(curso.instituicao)
                amostra.append(curso)
        return Resultado(amostra[:6], len(todos), True)
    encontrados = []
    for curso in todos:
        texto = _normalizar(" ".join((curso.curso, curso.instituicao, curso.unidade_organica, curso.localidade, curso.area)))
        if all(palavra in texto for palavra in palavras):
            encontrados.append(curso)
    # Primeiro os que têm o termo no nome do curso, depois por número de vagas.
    encontrados.sort(key=lambda c: (not all(p in _normalizar(c.curso) for p in palavras), -(c.vagas or 0)))
    return Resultado(encontrados[:limite], len(encontrados), False)


@dataclass(frozen=True)
class Resumo:
    cursos: int
    instituicoes: int
    vagas: int
    areas: tuple[str, ...]


def resumo(config: Mapping) -> Resumo:
    todos = cursos(config)
    return Resumo(
        cursos=len(todos),
        instituicoes=len({c.instituicao for c in todos}),
        vagas=sum(c.vagas or 0 for c in todos),
        areas=tuple(sorted({c.area for c in todos})),
    )


# ---------------------------------------------------------------------------
# US05: filtros, ficha e comparação
# ---------------------------------------------------------------------------

MAX_COMPARAR = 3   # RF34: comparar até 3 cursos lado a lado
MIN_COMPARAR = 2


@dataclass(frozen=True)
class Opcoes:
    """Os valores que existem no catálogo para cada filtro, por ordem alfabética (sem contar acentos)."""
    areas: tuple[str, ...]
    instituicoes: tuple[str, ...]
    localidades: tuple[str, ...]


def _ordenados(valores) -> tuple[str, ...]:
    return tuple(sorted(set(valores), key=_normalizar))


def opcoes(config: Mapping) -> Opcoes:
    todos = cursos(config)
    return Opcoes(
        areas=_ordenados(c.area for c in todos),
        instituicoes=_ordenados(c.instituicao for c in todos),
        localidades=_ordenados(c.localidade for c in todos),
    )


@dataclass(frozen=True)
class Filtros:
    termo: str = ""
    area: str = ""
    instituicao: str = ""
    localidade: str = ""

    @property
    def ativos(self) -> bool:
        return bool(self.termo or self.area or self.instituicao or self.localidade)


def ler_filtros(argumentos: Mapping, config: Mapping) -> Filtros:
    """Os filtros vêm do endereço (?q=…&area=…), para funcionarem sem JavaScript e poderem ser partilhados.

    Um valor que não existe no catálogo é ignorado (como se o filtro não tivesse sido escolhido).
    """
    disponiveis = opcoes(config)

    def valido(nome: str, permitidos: tuple[str, ...]) -> str:
        valor = (argumentos.get(nome) or "").strip()
        return valor if valor in permitidos else ""

    return Filtros(
        termo=(argumentos.get("q") or "").strip()[:80],
        area=valido("area", disponiveis.areas),
        instituicao=valido("instituicao", disponiveis.instituicoes),
        localidade=valido("localidade", disponiveis.localidades),
    )


def filtrar(config: Mapping, filtros: Filtros) -> list[Curso]:
    """Os cursos que respeitam todos os filtros. Sem filtros, o catálogo todo, por número de vagas."""
    palavras = _normalizar(filtros.termo).split()
    escolhidos = []
    for curso in cursos(config):
        if filtros.area and curso.area != filtros.area:
            continue
        if filtros.instituicao and curso.instituicao != filtros.instituicao:
            continue
        if filtros.localidade and curso.localidade != filtros.localidade:
            continue
        if palavras:
            texto = _normalizar(" ".join((curso.curso, curso.instituicao, curso.unidade_organica, curso.localidade, curso.area)))
            if not all(palavra in texto for palavra in palavras):
                continue
        escolhidos.append(curso)
    escolhidos.sort(key=lambda c: (bool(palavras) and not all(p in _normalizar(c.curso) for p in palavras), -(c.vagas or 0), _normalizar(c.curso)))
    return escolhidos


def por_chave(config: Mapping, chave: str) -> Curso | None:
    return next((c for c in cursos(config) if c.chave == chave), None)


@dataclass(frozen=True)
class Comparacao:
    cursos: list[Curso]
    ignorados: int        # chaves que não existem no catálogo ou repetidas
    a_mais: int           # cursos pedidos acima do máximo (só se comparam os primeiros 3)

    @property
    def suficiente(self) -> bool:
        return len(self.cursos) >= MIN_COMPARAR


def comparar(config: Mapping, chaves: list[str]) -> Comparacao:
    """Os cursos a comparar, pela ordem pedida, sem repetidos e só do catálogo; no máximo 3."""
    vistos, encontrados, ignorados = set(), [], 0
    for chave in chaves:
        curso = por_chave(config, chave)
        if curso is None or chave in vistos:
            ignorados += 1
            continue
        vistos.add(chave)
        encontrados.append(curso)
    return Comparacao(encontrados[:MAX_COMPARAR], ignorados, max(0, len(encontrados) - MAX_COMPARAR))
