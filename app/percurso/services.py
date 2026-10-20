"""Regras das decisões do percurso (US31): escolher um curso, mudar de curso e ver a linha do tempo.

- RN10: nada é escolhido automaticamente. Escolher exige confirmação (a rota mostra primeiro a
  página de confirmação e só o POST chama ``escolher``).
- RF03: o curso do perfil é o da decisão mais recente.
- RF35: cada decisão guarda a data, os cursos sugeridos nessa altura e o curso escolhido.
- Ponto 15 dos requisitos (decisão do PO, 20/10): depois de escolher, a conversa com o LLM é
  apagada; só fica a decisão.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from ..catalogo.repository import Curso
from ..orientacao import services as orientacao
from . import repository


class CursoInexistente(LookupError):
    """O identificador não existe no catálogo."""


class MesmoCurso(ValueError):
    """O curso escolhido já é o curso atual: não cria decisão nova."""


@dataclass(frozen=True)
class CursoSugerido:
    chave: str
    curso: str
    instituicao: str


@dataclass(frozen=True)
class Decisao:
    curso_chave: str
    curso: str
    instituicao: str
    origem: str                              # "sugestao" ou "catalogo"
    sugeridos: tuple[CursoSugerido, ...]     # o que o assistente tinha sugerido nessa altura
    decidida_em: datetime

    @property
    def veio_das_sugestoes(self) -> bool:
        return self.origem == "sugestao"


def _agora() -> datetime:
    return datetime.now(timezone.utc)


def _decisao(linha: sqlite3.Row) -> Decisao:
    sugeridos = tuple(CursoSugerido(s["chave"], s["curso"], s["instituicao"]) for s in json.loads(linha["sugeridos"]))
    return Decisao(
        curso_chave=linha["curso_chave"],
        curso=linha["curso"],
        instituicao=linha["instituicao"],
        origem=linha["origem"],
        sugeridos=sugeridos,
        decidida_em=datetime.fromisoformat(linha["decidida_em"]),
    )


def decisoes(db: sqlite3.Connection, user_id: int) -> list[Decisao]:
    """A linha do tempo: da decisão mais recente para a mais antiga."""
    return [_decisao(linha) for linha in repository.listar(db, user_id)]


def curso_atual(db: sqlite3.Connection, user_id: int) -> Decisao | None:
    """O curso do perfil (RF03): o da decisão mais recente, ou None se ainda não escolheu."""
    todas = decisoes(db, user_id)
    return todas[0] if todas else None


def curso_do_catalogo(chave: str, catalogo: Sequence[Curso]) -> Curso:
    """O curso com este identificador, ou ``CursoInexistente`` (só se escolhem cursos do catálogo)."""
    for curso in catalogo:
        if curso.chave == chave:
            return curso
    raise CursoInexistente(chave)


def _sugeridos_agora(db: sqlite3.Connection, user_id: int, catalogo: Sequence[Curso]) -> tuple[CursoSugerido, ...]:
    """Os cursos que a conversa de orientação sugeriu, se terminou com sugestões (validados, RN09)."""
    sugestao = orientacao.cursos_sugeridos(orientacao.obter(db, user_id), catalogo)
    if sugestao is None:
        return ()
    return tuple(CursoSugerido(s.curso.chave, s.curso.curso, s.curso.instituicao) for s in sugestao.cursos)


def escolher(db: sqlite3.Connection, user_id: int, chave: str, catalogo: Sequence[Curso]) -> Decisao:
    """Regista a escolha confirmada pelo aluno e apaga a conversa de orientação (ponto 15).

    Levanta ``CursoInexistente`` se o curso não estiver no catálogo e ``MesmoCurso`` se já for o
    curso atual (mudar de curso cria uma decisão nova; escolher o mesmo não).
    """
    curso = curso_do_catalogo(chave, catalogo)
    atual = curso_atual(db, user_id)
    if atual is not None and atual.curso_chave == chave:
        raise MesmoCurso(chave)
    sugeridos = _sugeridos_agora(db, user_id, catalogo)
    origem = "sugestao" if any(s.chave == chave for s in sugeridos) else "catalogo"
    agora = _agora()
    repository.inserir(
        db,
        user_id,
        curso_chave=curso.chave,
        curso=curso.curso,
        instituicao=curso.instituicao,
        origem=origem,
        sugeridos=json.dumps([s.__dict__ for s in sugeridos], ensure_ascii=False),
        decidida_em=agora.isoformat(timespec="microseconds"),
    )
    orientacao.recomecar(db, user_id)
    return Decisao(curso.chave, curso.curso, curso.instituicao, origem, sugeridos, agora)
