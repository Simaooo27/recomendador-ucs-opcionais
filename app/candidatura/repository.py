"""Consultas SQL à tabela ``planos_candidatura`` (padrão Repository). Só este ficheiro tem SQL do plano."""
from __future__ import annotations

import sqlite3


def obter(db: sqlite3.Connection, user_id: int) -> sqlite3.Row | None:
    return db.execute(
        "SELECT media, exames, opcoes, atualizado_em FROM planos_candidatura WHERE user_id = ?", (user_id,)
    ).fetchone()


def por_partilha(db: sqlite3.Connection, codigo: str) -> sqlite3.Row | None:
    """O plano partilhado com este código, com o nome da pessoa (só o nome; nunca o email)."""
    return db.execute(
        """
        SELECT p.user_id, p.media, p.exames, p.opcoes, u.nome
          FROM planos_candidatura p JOIN users u ON u.id = p.user_id
         WHERE p.partilha = ?
        """,
        (codigo,),
    ).fetchone()


def mudar_partilha(db: sqlite3.Connection, user_id: int, codigo: str | None) -> None:
    db.execute("UPDATE planos_candidatura SET partilha = ? WHERE user_id = ?", (codigo, user_id))
    db.commit()


def partilha(db: sqlite3.Connection, user_id: int) -> str | None:
    linha = db.execute("SELECT partilha FROM planos_candidatura WHERE user_id = ?", (user_id,)).fetchone()
    return linha["partilha"] if linha else None


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
