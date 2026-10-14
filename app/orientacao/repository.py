"""Consultas SQL à tabela ``conversas_orientacao`` (padrão Repository). Só este ficheiro tem SQL da orientação."""
from __future__ import annotations

import sqlite3


def obter(db: sqlite3.Connection, user_id: int) -> sqlite3.Row | None:
    return db.execute(
        "SELECT mensagens, sugestao, atualizada_em FROM conversas_orientacao WHERE user_id = ?", (user_id,)
    ).fetchone()


def guardar(db: sqlite3.Connection, user_id: int, mensagens: str, sugestao: str | None, agora: str) -> None:
    db.execute(
        """
        INSERT INTO conversas_orientacao (user_id, mensagens, sugestao, atualizada_em) VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            mensagens = excluded.mensagens, sugestao = excluded.sugestao, atualizada_em = excluded.atualizada_em
        """,
        (user_id, mensagens, sugestao, agora),
    )
    db.commit()


def apagar(db: sqlite3.Connection, user_id: int) -> None:
    db.execute("DELETE FROM conversas_orientacao WHERE user_id = ?", (user_id,))
    db.commit()
