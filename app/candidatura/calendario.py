"""Datas do Concurso Nacional de Acesso (US38): as 3 fases e o próximo prazo.

As datas vêm de ``dados/calendario-concurso.csv``, copiadas do despacho que a DGES publica todos os
anos (o de 2026 é o Despacho n.º 6934/2026). Quando sair o calendário do ano seguinte, a equipa
acrescenta as linhas desse ano ao ficheiro; o OptaBem mostra o ano mais recente.

Sem Flask nem base de dados: ``proximo_prazo`` é uma função pura, para ser testada com qualquer dia.
"""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path

from .. import texts

# Página da DGES com o calendário oficial (critério da US38: ligação para a DGES).
PAGINA_DGES = "https://www.dges.gov.pt/pt/pagina/calendario-concurso-nacional-de-acesso-0"

ETAPAS = ("candidatura", "resultados", "matricula")


@dataclass(frozen=True)
class Etapa:
    ano: int
    fase: int          # 1, 2 ou 3
    etapa: str         # «candidatura», «resultados» ou «matricula»
    inicio: date
    fim: date          # igual ao início quando é um só dia (por exemplo, os resultados)
    nota: str = ""

    @property
    def nome(self) -> str:
        """«Candidatura», «Resultados» ou «Matrícula e inscrição» (app/texts.py)."""
        return getattr(texts, f"CALENDARIO_ETAPA_{self.etapa.upper()}")

    @property
    def um_dia(self) -> bool:
        return self.inicio == self.fim

    def a_decorrer(self, hoje: date) -> bool:
        return self.inicio <= hoje <= self.fim


@dataclass(frozen=True)
class Fase:
    numero: int
    etapas: tuple[Etapa, ...]   # pela ordem de ETAPAS


@dataclass(frozen=True)
class Calendario:
    ano: int | None              # None = o ficheiro não tem datas
    fases: tuple[Fase, ...]

    @property
    def etapas(self) -> tuple[Etapa, ...]:
        return tuple(sorted((e for f in self.fases for e in f.etapas), key=lambda e: (e.inicio, e.fim)))


@dataclass(frozen=True)
class Prazo:
    etapa: Etapa | None          # None = já passaram todas as datas publicadas
    a_decorrer: bool = False
    ano_seguinte: int | None = None   # quando não há prazo: o ano cujas datas ainda não saíram


def _ler_data(texto: str) -> date:
    return date.fromisoformat(texto.strip())


@lru_cache(maxsize=4)
def _ler(caminho: str, modificado: float) -> tuple[Etapa, ...]:
    etapas = []
    with open(caminho, encoding="utf-8-sig", newline="") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            if linha["etapa"] not in ETAPAS:
                raise ValueError(f"Etapa desconhecida em {caminho}: {linha['etapa']!r}")
            inicio = _ler_data(linha["inicio"])
            fim = _ler_data(linha["fim"] or linha["inicio"])
            if fim < inicio:
                raise ValueError(f"Em {caminho}, a etapa {linha['etapa']} da {linha['fase']}.ª fase acaba antes de começar")
            etapas.append(Etapa(int(linha["ano"]), int(linha["fase"]), linha["etapa"], inicio, fim, (linha.get("nota") or "").strip()))
    return tuple(etapas)


def ler(caminho: str | Path) -> Calendario:
    """O calendário do ano mais recente do ficheiro. Sem ficheiro, um calendário vazio."""
    caminho = str(caminho)
    if not os.path.exists(caminho):
        return Calendario(None, ())
    todas = _ler(caminho, os.path.getmtime(caminho))   # relê quando o ficheiro muda
    if not todas:
        return Calendario(None, ())
    ano = max(e.ano for e in todas)
    do_ano = [e for e in todas if e.ano == ano]
    fases = []
    for numero in sorted({e.fase for e in do_ano}):
        etapas = sorted((e for e in do_ano if e.fase == numero), key=lambda e: ETAPAS.index(e.etapa))
        fases.append(Fase(numero, tuple(etapas)))
    return Calendario(ano, tuple(fases))


def proximo_prazo(calendario: Calendario, hoje: date) -> Prazo:
    """A etapa a decorrer hoje ou, se não houver, a próxima a começar.

    Se duas etapas estão a decorrer ao mesmo tempo (a matrícula da 1.ª fase e a candidatura à 2.ª),
    conta a que acaba primeiro. Depois da última data publicada, ``etapa`` é None e ``ano_seguinte``
    diz de que ano são as datas que ainda não saíram.
    """
    a_decorrer = [e for e in calendario.etapas if e.a_decorrer(hoje)]
    if a_decorrer:
        return Prazo(min(a_decorrer, key=lambda e: (e.fim, e.inicio)), a_decorrer=True)
    futuras = [e for e in calendario.etapas if e.inicio > hoje]
    if futuras:
        return Prazo(futuras[0])
    ano_seguinte = (calendario.ano + 1) if calendario.ano is not None else hoje.year
    return Prazo(None, ano_seguinte=max(ano_seguinte, hoje.year))


def data_curta(dia: date) -> str:
    """2026-08-06 -> «06/08/2026»."""
    return f"{dia:%d/%m/%Y}"


def frase_do_prazo(prazo: Prazo) -> str:
    """A frase do passo atual do percurso: «Candidatura da 1.ª fase: até 06/08/2026.»"""
    etapa = prazo.etapa
    if etapa is None:
        return texts.HOME_PRAZO_SEM_DATAS.format(ano=prazo.ano_seguinte)
    nome = etapa.nome
    inicio, fim = data_curta(etapa.inicio), data_curta(etapa.fim)
    if prazo.a_decorrer:
        modelo = texts.HOME_PRAZO_A_DECORRER_DIA if etapa.um_dia else texts.HOME_PRAZO_A_DECORRER
        return modelo.format(etapa=nome, fase=etapa.fase, fim=fim)
    if etapa.um_dia:
        return texts.HOME_PRAZO_FUTURO_DIA.format(etapa=nome, fase=etapa.fase, inicio=inicio)
    return texts.HOME_PRAZO_FUTURO.format(etapa=nome, fase=etapa.fase, inicio=inicio, fim=fim)
