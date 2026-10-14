"""Pesquisa no catálogo de cursos (página de apresentação; base da US05)."""
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
