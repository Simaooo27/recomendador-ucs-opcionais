"""Consultas SQL à tabela ``planos_candidatura`` (padrão Repository). Só este ficheiro tem SQL do plano."""
from __future__ import annotations

import sqlite3


def obter(db: sqlite3.Connection, user_id: int) -> sqlite3.Row | None:
    return db.execute(
        "SELECT media, exames, opcoes, atualizado_em FROM planos_candidatura WHERE user_id = ?", (user_id,)
    ).fetchone()


def guardar(db: sqlite3.Connection, user_id: int, media: float | None, exames: str, opcoes: str, agora: str) -> None:
    db.execute(
        """
        INSERT INTO planos_candidatura (user_id, media, exames, opcoes, atualizado_em) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            media = excluded.media, exames = excluded.exames, opcoes = excluded.opcoes,
            atualizado_em = excluded.atualizado_em
        """,
        (user_id, media, exames, opcoes, agora),
    )
    db.commit()
