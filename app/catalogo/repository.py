"""Leitura do catálogo de cursos a partir do CSV da DGES (dados/catalogo-cursos-mvp.csv).

Só este ficheiro sabe de onde vêm os cursos. A US04 vai trocá-lo por consultas à base de
dados, com a mesma função ``todos`` (padrão Repository).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Curso:
    codigo_instituicao: str
    codigo_curso: str
    curso: str
    instituicao: str
    unidade_organica: str
    localidade: str
    tipo_ensino: str
    area: str
    vagas: int | None
    ultimo_colocado: str | None   # nota de candidatura, como a DGES a escreve (ex.: «138,3»)
    descricao: str
    saidas: str
    fonte: str                    # página da DGES com os dados de acesso

    @property
    def chave(self) -> str:
        return f"{self.codigo_instituicao}-{self.codigo_curso}"


def _inteiro(valor: str) -> int | None:
    valor = (valor or "").strip()
    return int(valor) if valor.isdigit() else None


@lru_cache(maxsize=4)
def _ler(caminho: str, modificado: float) -> tuple[Curso, ...]:
    with open(caminho, encoding="utf-8-sig", newline="") as ficheiro:
        linhas = list(csv.DictReader(ficheiro))
    return tuple(
        Curso(
            codigo_instituicao=l["codigo_instituicao_dges"].strip(),
            codigo_curso=l["codigo_curso_dges"].strip(),
            curso=l["curso"].strip(),
            instituicao=l["instituicao"].strip(),
            unidade_organica=l["unidade_organica"].strip(),
            localidade=l["localidade"].strip(),
            tipo_ensino=l["tipo_ensino"].strip(),
            area=l["area_optabem"].strip(),
            vagas=_inteiro(l["vagas_2026"]),
            ultimo_colocado=l["ultimo_colocado_1fase_2025"].strip() or None,
            descricao=l["descricao"].strip(),
            saidas=l["saidas_profissionais"].strip(),
            fonte=l["fonte_dados_acesso"].strip(),
        )
        for l in linhas
        if l.get("curso", "").strip()
    )


def todos(caminho: str | Path) -> tuple[Curso, ...]:
    """Todos os cursos do ficheiro. Volta a ler o ficheiro se ele for alterado."""
    caminho = Path(caminho)
    if not caminho.exists():
        return ()
    return _ler(str(caminho), caminho.stat().st_mtime)
