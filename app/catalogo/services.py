"""Catálogo de cursos: pesquisa (página de apresentação), filtros, ficha e comparação (US05).

Tudo funciona sem sessão iniciada (RF34). Os cursos vêm de ``repository.todos`` (o CSV da DGES),
com as correções da gestão por cima (US39): ``cursos`` é o único ponto por onde o resto da
aplicação lê o catálogo, por isso um curso corrigido ou escondido muda em todo o lado (ficha,
pesquisa, comparação, conversa com o assistente e plano de candidatura).
"""
from __future__ import annotations

import re
import sqlite3
import unicodedata
from dataclasses import dataclass, replace
from typing import Iterable, Mapping

from . import correcoes_repository, repository
from .repository import Curso


def _normalizar(texto: str) -> str:
    """Minúsculas e sem acentos, para «informatica» encontrar «Informática»."""
    decomposto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def _palavras_do_texto(texto: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", _normalizar(texto))


def _corresponde(palavras: list[str], *campos: str) -> bool:
    """Cada palavra pesquisada tem de ser o início de uma palavra dos campos («gest» encontra
    «Gestão»; «ti» já não encontra «Informática»). Revisão estética de 23/10: a procura por
    pedaços do meio das palavras trazia cursos sem relação com o que se escreveu."""
    existentes = _palavras_do_texto(" ".join(campos))
    return all(any(e.startswith(p) for e in existentes) for p in palavras)


def _campos_pesquisados(curso: Curso) -> tuple[str, ...]:
    """Onde se procura: nome do curso, instituição, localidade e área. A escola ou faculdade
    (unidade orgânica) fica de fora a 23/10 (decisão do PO): «gestão» encontrava Engenharia
    Informática só por ser dada numa «Escola Superior de Tecnologia e Gestão»."""
    return (curso.curso, curso.instituicao, curso.localidade, curso.area)


def _relevancia(palavras: list[str], curso: Curso) -> int:
    """Ordem dos resultados: 0 = o nome do curso é exatamente o que se escreveu («Gestão»),
    1 = o termo está no nome do curso, 2 = só na instituição, localidade ou área."""
    if _palavras_do_texto(curso.curso) == palavras:
        return 0
    return 1 if _corresponde(palavras, curso.curso) else 2


@dataclass(frozen=True)
class Correcao:
    """O que a gestão mudou num curso (US39). ``None`` = fica o texto da DGES."""

    descricao: str | None = None
    saidas: str | None = None
    escondido: bool = False
    alterado_por: str = ""
    alterado_em: str = ""


def _correcao(linha: sqlite3.Row) -> Correcao:
    return Correcao(linha["descricao"], linha["saidas"], bool(linha["escondido"]), linha["alterado_por"], linha["alterado_em"])


def correcoes(db: sqlite3.Connection) -> dict[str, Correcao]:
    return {linha["curso_chave"]: _correcao(linha) for linha in correcoes_repository.todas(db)}


def corrigido(curso: Curso, correcao: Correcao | None) -> Curso:
    """O curso com a descrição e as saídas corrigidas (função pura)."""
    if correcao is None:
        return curso
    campos = {}
    if correcao.descricao is not None:
        campos["descricao"] = correcao.descricao
    if correcao.saidas is not None:
        campos["saidas"] = correcao.saidas
    return replace(curso, **campos) if campos else curso


def aplicar_correcoes(base: Iterable[Curso], por_chave: Mapping[str, Correcao]) -> tuple[Curso, ...]:
    """Os cursos que os alunos veem: corrigidos e sem os escondidos (função pura)."""
    resultado = []
    for curso in base:
        correcao = por_chave.get(curso.chave)
        if correcao is not None and correcao.escondido:
            continue
        resultado.append(corrigido(curso, correcao))
    return tuple(resultado)


def _ligacao_atual() -> sqlite3.Connection | None:
    """A base de dados do pedido atual, se houver (fora da aplicação, por exemplo num script, não há)."""
    from flask import has_app_context

    if not has_app_context():
        return None
    from ..db import get_db

    return get_db()


def cursos(config: Mapping, db: sqlite3.Connection | None = None) -> tuple[Curso, ...]:
    """O catálogo que os alunos veem: o da DGES com as correções da gestão (US39)."""
    base = repository.todos(config["CATALOGO_CSV"])
    db = db if db is not None else _ligacao_atual()
    if db is None:
        return base
    por_chave = correcoes(db)
    return aplicar_correcoes(base, por_chave) if por_chave else base


def cursos_para_gestao(config: Mapping, db: sqlite3.Connection) -> list[tuple[Curso, Correcao | None]]:
    """Todos os cursos, também os escondidos, já corrigidos, com a correção de cada um (US39)."""
    por_chave = correcoes(db)
    return [(corrigido(c, por_chave.get(c.chave)), por_chave.get(c.chave)) for c in repository.todos(config["CATALOGO_CSV"])]


def corresponde(curso: Curso, termo: str) -> bool:
    """O curso corresponde ao termo (as mesmas regras da pesquisa do catálogo). Termo vazio: sim."""
    palavras = _palavras_do_texto(termo or "")
    return not palavras or _corresponde(palavras, *_campos_pesquisados(curso))


@dataclass(frozen=True)
class Resultado:
    cursos: list[Curso]   # os que se mostram (no máximo ``limite``)
    total: int            # quantos cursos correspondem ao termo
    amostra: bool         # True quando não havia termo e se mostra uma amostra


def pesquisar(config: Mapping, termo: str, limite: int = 60) -> Resultado:
    """Cursos em que todas as palavras do termo começam uma palavra do nome, instituição, localidade ou área.

    Sem termo, devolve uma amostra variada (um curso de cada instituição, por ordem de vagas).
    """
    todos = cursos(config)
    palavras = _palavras_do_texto(termo or "")
    if not palavras:
        vistos, amostra = set(), []
        for curso in sorted(todos, key=lambda c: -(c.vagas or 0)):
            if curso.instituicao not in vistos:
                vistos.add(curso.instituicao)
                amostra.append(curso)
        return Resultado(amostra[:6], len(todos), True)
    encontrados = []
    for curso in todos:
        if _corresponde(palavras, *_campos_pesquisados(curso)):
            encontrados.append(curso)
    # Primeiro os que têm o termo no nome do curso, depois por número de vagas.
    encontrados.sort(key=lambda c: (_relevancia(palavras, c), -(c.vagas or 0)))
    return Resultado(encontrados[:limite], len(encontrados), False)


@dataclass(frozen=True)
class Resumo:
    cursos: int
    instituicoes: int
    vagas: int
    areas: tuple[str, ...]


AREAS_NA_APRESENTACAO = 5   # «Ou veja por área»: só as áreas com mais cursos (o catálogo tem muitas)


def _areas_principais(todos) -> tuple[str, ...]:
    contagem: dict[str, int] = {}
    for curso in todos:
        if curso.area:
            contagem[curso.area] = contagem.get(curso.area, 0) + 1
    principais = sorted(contagem, key=lambda a: (-contagem[a], _normalizar(a)))[:AREAS_NA_APRESENTACAO]
    return tuple(sorted(principais, key=_normalizar))


def resumo(config: Mapping) -> Resumo:
    todos = cursos(config)
    return Resumo(
        cursos=len(todos),
        instituicoes=len({c.instituicao for c in todos}),
        vagas=sum(c.vagas or 0 for c in todos),
        areas=_areas_principais(todos),
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
    palavras = _palavras_do_texto(filtros.termo)
    escolhidos = []
    for curso in cursos(config):
        if filtros.area and curso.area != filtros.area:
            continue
        if filtros.instituicao and curso.instituicao != filtros.instituicao:
            continue
        if filtros.localidade and curso.localidade != filtros.localidade:
            continue
        if palavras and not _corresponde(palavras, *_campos_pesquisados(curso)):
            continue
        escolhidos.append(curso)
    escolhidos.sort(key=lambda c: (_relevancia(palavras, c) if palavras else 0, -(c.vagas or 0), _normalizar(c.curso)))
    return escolhidos


POR_PAGINA = 24   # cursos por página em /cursos/ (o catálogo completo tem mais de mil)


@dataclass(frozen=True)
class Pagina:
    cursos: list[Curso]
    numero: int        # 1, 2, …
    paginas: int       # total de páginas (pelo menos 1)
    total: int         # cursos que respeitam os filtros

    @property
    def anterior(self) -> int | None:
        return self.numero - 1 if self.numero > 1 else None

    @property
    def seguinte(self) -> int | None:
        return self.numero + 1 if self.numero < self.paginas else None


def paginar(cursos_filtrados: list[Curso], pedido: str | None) -> Pagina:
    """A página ``pedido`` (texto do endereço, ?p=2). Um número inválido dá a primeira ou a última."""
    paginas = max(1, -(-len(cursos_filtrados) // POR_PAGINA))
    numero = int(pedido) if (pedido or "").isdigit() else 1
    numero = min(max(numero, 1), paginas)
    inicio = (numero - 1) * POR_PAGINA
    return Pagina(cursos_filtrados[inicio:inicio + POR_PAGINA], numero, paginas, len(cursos_filtrados))


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
