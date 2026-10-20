"""Consultas SQL à tabela ``decisoes`` (padrão Repository). Só este ficheiro tem SQL do percurso."""
from __future__ import annotations

import sqlite3


def inserir(
    db: sqlite3.Connection,
    user_id: int,
    *,
    curso_chave: str,
    curso: str,
    instituicao: str,
    origem: str,
    sugeridos: str,
    decidida_em: str,
) -> int:
    cursor = db.execute(
        """
        INSERT INTO decisoes (user_id, curso_chave, curso, instituicao, origem, sugeridos, decidida_em)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, curso_chave, curso, instituicao, origem, sugeridos, decidida_em),
    )
    db.commit()
    return cursor.lastrowid


def listar(db: sqlite3.Connection, user_id: int) -> list[sqlite3.Row]:
    """Decisões do utilizador, da mais recente para a mais antiga."""
    return db.execute(
        """
        SELECT id, curso_chave, curso, instituicao, origem, sugeridos, decidida_em
        FROM decisoes WHERE user_id = ? ORDER BY decidida_em DESC, id DESC
        """,
        (user_id,),
    ).fetchall()
