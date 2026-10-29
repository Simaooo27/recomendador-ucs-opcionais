"""Regras do plano de candidatura: notas do aluno, opções (até 6, por ordem) e avisos.

As contas estão em ``calculos.py``. Aqui só se lê e guarda o plano e se decide o que mostrar.
"""
from __future__ import annotations

import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping, Sequence

from .. import texts
from ..catalogo.repository import Curso
from . import repository
from .calculos import (
    Combinacao, Necessidade, Notas, Simulacao, Situacao, chega_na_2a_fase, exames_que_abrem_portas, ler_numero,
    nota_de_exame, nota_necessaria, simular,
)

MAX_OPCOES = 6   # o Concurso Nacional de Acesso aceita até 6 pares instituição/curso


@dataclass(frozen=True)
class Plano:
    notas: Notas
    opcoes: tuple[str, ...]   # chaves do catálogo, pela ordem da candidatura

    @property
    def tem_notas(self) -> bool:
        return self.notas.media is not None

    @property
    def cheio(self) -> bool:
        return len(self.opcoes) >= MAX_OPCOES


@dataclass(frozen=True)
class Opcao:
    posicao: int
    curso: Curso
    simulacao: Simulacao
    necessidade: Necessidade | None = None   # quanto precisa nas provas em falta (23/10)


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def obter(db: sqlite3.Connection, user_id: int) -> Plano:
    linha = repository.obter(db, user_id)
    if linha is None:
        return Plano(Notas(), ())
    exames = {codigo: float(valor) for codigo, valor in json.loads(linha["exames"]).items()}
    return Plano(Notas(linha["media"], exames), tuple(json.loads(linha["opcoes"])))


def _guardar(db: sqlite3.Connection, user_id: int, plano: Plano) -> None:
    repository.guardar(
        db, user_id, plano.notas.media, json.dumps(dict(plano.notas.exames), sort_keys=True),
        json.dumps(list(plano.opcoes)), _agora(),
    )


# -- Notas ----------------------------------------------------------------------------------------

def ler_notas(formulario: Mapping[str, str], codigos: Sequence[str]) -> tuple[Notas, dict[str, str]]:
    """Lê o formulário das notas. Devolve as notas e os erros ({campo: mensagem})."""
    erros: dict[str, str] = {}
    texto_media = (formulario.get("media") or "").strip()
    media = ler_numero(texto_media)
    if not texto_media:
        erros["media"] = texts.CANDIDATURA_ERRO_MEDIA_VAZIA
    elif media is None or not 9.5 <= media <= 20:
        erros["media"] = texts.CANDIDATURA_ERRO_MEDIA
    exames: dict[str, float] = {}
    for codigo in codigos:
        texto = (formulario.get(f"exame_{codigo}") or "").strip()
        if not texto:
            continue
        valor = nota_de_exame(texto)
        if valor is None or not 0 <= valor <= 200:
            erros[f"exame_{codigo}"] = texts.CANDIDATURA_ERRO_EXAME
        else:
            exames[codigo] = valor
    return Notas(media if "media" not in erros else None, exames), erros


def guardar_notas(db: sqlite3.Connection, user_id: int, notas: Notas) -> None:
    plano = obter(db, user_id)
    _guardar(db, user_id, Plano(notas, plano.opcoes))


# -- Opções ---------------------------------------------------------------------------------------

class PlanoCheio(ValueError):
    """Já há 6 opções."""


def juntar(db: sqlite3.Connection, user_id: int, chave: str) -> bool:
    """Junta um curso ao fim da lista. False se já lá estava; ``PlanoCheio`` se já há 6."""
    plano = obter(db, user_id)
    if chave in plano.opcoes:
        return False
    if plano.cheio:
        raise PlanoCheio(chave)
    _guardar(db, user_id, Plano(plano.notas, plano.opcoes + (chave,)))
    return True


def retirar(db: sqlite3.Connection, user_id: int, chave: str) -> None:
    plano = obter(db, user_id)
    _guardar(db, user_id, Plano(plano.notas, tuple(c for c in plano.opcoes if c != chave)))


def mover(db: sqlite3.Connection, user_id: int, chave: str, passo: int) -> None:
    """Sobe (passo −1) ou desce (passo +1) uma opção na lista."""
    plano = obter(db, user_id)
    opcoes = list(plano.opcoes)
    if chave not in opcoes:
        return
    i = opcoes.index(chave)
    j = i + passo
    if 0 <= j < len(opcoes):
        opcoes[i], opcoes[j] = opcoes[j], opcoes[i]
        _guardar(db, user_id, Plano(plano.notas, tuple(opcoes)))


def opcoes(plano: Plano, cursos: Sequence[Curso]) -> list[Opcao]:
    """As opções do plano com a simulação de cada uma. Um curso que saiu do catálogo não aparece."""
    por_chave = {c.chave: c for c in cursos}
    resultado = []
    for chave in plano.opcoes:
        curso = por_chave.get(chave)
        if curso is not None:
            resultado.append(Opcao(len(resultado) + 1, curso, simular(curso, plano.notas), nota_necessaria(curso, plano.notas)))
    return resultado


def avisos(plano: Plano, lista: Sequence[Opcao]) -> list[str]:
    """O que convém rever antes de submeter a candidatura no site da DGES."""
    if not lista:
        return []
    resultado = []
    nao_contam = [o for o in lista if o.simulacao.situacao in (Situacao.FALTA_PROVA, Situacao.ABAIXO_DO_MINIMO, Situacao.FORA_DO_CONCURSO)]
    if nao_contam:
        resultado.append(texts.CANDIDATURA_AVISO_NAO_CONTAM.format(n=len(nao_contam)))
    if plano.tem_notas:
        seguras = [o for o in lista if o.simulacao.situacao in (Situacao.ACIMA, Situacao.SEM_REFERENCIA)]
        if not seguras:
            resultado.append(texts.CANDIDATURA_AVISO_SEM_SEGURA)
        primeira = lista[0]
        mais_dificeis = [
            o for o in lista[1:]
            if o.simulacao.situacao.conta and o.curso.ultimo_colocado_numero and primeira.curso.ultimo_colocado_numero
            and o.curso.ultimo_colocado_numero > primeira.curso.ultimo_colocado_numero
        ]
        if primeira.simulacao.situacao is Situacao.ACIMA and mais_dificeis:
            resultado.append(texts.CANDIDATURA_AVISO_ORDEM.format(curso=primeira.curso.curso))
    if len(lista) < MAX_OPCOES:
        resultado.append(texts.CANDIDATURA_AVISO_MENOS_DE_6.format(n=len(lista), livres=MAX_OPCOES - len(lista)))
    if any(o.curso.pre_requisitos for o in lista):
        resultado.append(texts.CANDIDATURA_AVISO_PRE_REQUISITOS)
    return resultado


def sugestoes(plano: Plano, cursos: Sequence[Curso], area: str, limite: int = 3) -> list[tuple[Curso, Simulacao]]:
    """Cursos da mesma área, fora do plano, onde o aluno fica acima ou perto do último colocado."""
    if not plano.tem_notas or not area:
        return []
    encontrados = []
    for curso in cursos:
        if curso.area != area or curso.chave in plano.opcoes:
            continue
        simulacao = simular(curso, plano.notas)
        if simulacao.situacao in (Situacao.ACIMA, Situacao.PERTO):
            encontrados.append((curso, simulacao))
    # Primeiro os cursos onde está acima, do mais disputado para o menos; depois os «perto».
    encontrados.sort(key=lambda par: (par[1].situacao is not Situacao.ACIMA, abs(par[1].diferenca or 0)))
    return encontrados[:limite]


# -- Exames que abrem mais portas e plano B (23/10) -----------------------------------------------

def exames_do_plano(plano: Plano, lista: Sequence[Opcao]) -> list[Combinacao]:
    """Que combinação de exames serve para mais opções do plano (precisa de 2 ou mais opções)."""
    return exames_que_abrem_portas([o.curso for o in lista], plano.notas)


def plano_b(plano: Plano, lista: Sequence[Opcao], cursos: Sequence[Curso], limite: int = 3) -> list[tuple[Curso, Simulacao]]:
    """Cursos das áreas do plano, fora dele, que em 2025 tiveram vagas na 2.ª fase e a que a nota da
    pessoa chegava. Primeiro os mais disputados (último colocado da 2.ª fase mais alto)."""
    if not plano.tem_notas or not lista:
        return []
    areas = {o.curso.area for o in lista}
    encontrados = []
    for curso in cursos:
        if curso.area not in areas or curso.chave in plano.opcoes:
            continue
        simulacao = chega_na_2a_fase(curso, plano.notas)
        if simulacao is not None:
            encontrados.append((curso, simulacao))
    encontrados.sort(key=lambda par: -(par[0].ultimo_colocado_2fase_numero or 0))
    return encontrados[:limite]


# -- Partilhar (23/10) ----------------------------------------------------------------------------
# Uma ligação só de leitura para mostrar o plano a pais, a um explicador ou a um colega. Quem tem a
# ligação vê o primeiro nome, as opções, a nota de candidatura e a situação em cada uma; nunca vê o
# email, a média nem as notas dos exames. Desligar a partilha invalida a ligação de imediato.

def partilhar(db: sqlite3.Connection, user_id: int) -> str:
    """Liga a partilha (se ainda não estiver ligada) e devolve o código da ligação."""
    atual = repository.partilha(db, user_id)
    if atual:
        return atual
    if repository.obter(db, user_id) is None:
        _guardar(db, user_id, Plano(Notas(), ()))
    codigo = secrets.token_urlsafe(16)
    repository.mudar_partilha(db, user_id, codigo)
    return codigo


def deixar_de_partilhar(db: sqlite3.Connection, user_id: int) -> None:
    repository.mudar_partilha(db, user_id, None)


def codigo_de_partilha(db: sqlite3.Connection, user_id: int) -> str | None:
    return repository.partilha(db, user_id)


@dataclass(frozen=True)
class PlanoPartilhado:
    nome: str            # primeiro nome (pode estar vazio em contas antigas)
    opcoes: list[Opcao]


def plano_partilhado(db: sqlite3.Connection, codigo: str, cursos: Sequence[Curso]) -> PlanoPartilhado | None:
    if not codigo or len(codigo) > 64:
        return None
    linha = repository.por_partilha(db, codigo)
    if linha is None:
        return None
    exames = {c: float(v) for c, v in json.loads(linha["exames"]).items()}
    plano = Plano(Notas(linha["media"], exames), tuple(json.loads(linha["opcoes"])))
    primeiro = (linha["nome"] or "").split()
    return PlanoPartilhado(primeiro[0] if primeiro else "", opcoes(plano, cursos))
