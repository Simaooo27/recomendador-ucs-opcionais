"""Consultas SQL às correções do catálogo feitas na gestão (US39). Só este ficheiro tem esse SQL.

Os cursos vêm do CSV da DGES (``repository.py``); estas tabelas guardam só o que um administrador
corrigiu ou escondeu, e o histórico dessas alterações. Não tocam em dados de alunos.
"""
from __future__ import annotations

import sqlite3


def todas(db: sqlite3.Connection) -> list[sqlite3.Row]:
    return db.execute(
        "SELECT curso_chave, descricao, saidas, escondido, alterado_por, alterado_em FROM correcoes_cursos"
    ).fetchall()


def obter(db: sqlite3.Connection, chave: str) -> sqlite3.Row | None:
    return db.execute(
        "SELECT curso_chave, descricao, saidas, escondido, alterado_por, alterado_em FROM correcoes_cursos WHERE curso_chave = ?",
        (chave,),
    ).fetchone()


def guardar(
    db: sqlite3.Connection, chave: str, *, descricao: str | None, saidas: str | None, escondido: bool, por: str, em: str
) -> None:
    db.execute(
        """
        INSERT INTO correcoes_cursos (curso_chave, descricao, saidas, escondido, alterado_por, alterado_em)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(curso_chave) DO UPDATE SET
            descricao = excluded.descricao, saidas = excluded.saidas, escondido = excluded.escondido,
            alterado_por = excluded.alterado_por, alterado_em = excluded.alterado_em
        """,
        (chave, descricao, saidas, int(escondido), por, em),
    )


def apagar(db: sqlite3.Connection, chave: str) -> None:
    db.execute("DELETE FROM correcoes_cursos WHERE curso_chave = ?", (chave,))


def registar(db: sqlite3.Connection, chave: str, alteracao: str, por: str, em: str) -> None:
    db.execute(
        "INSERT INTO historico_catalogo (curso_chave, alteracao, alterado_por, alterado_em) VALUES (?, ?, ?, ?)",
        (chave, alteracao, por, em),
    )


def historico(db: sqlite3.Connection, chave: str) -> list[sqlite3.Row]:
    """As alterações de um curso, da mais recente para a mais antiga."""
    return db.execute(
        "SELECT alteracao, alterado_por, alterado_em FROM historico_catalogo WHERE curso_chave = ? ORDER BY alterado_em DESC, id DESC",
        (chave,),
    ).fetchall()
