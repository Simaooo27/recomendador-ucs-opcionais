"""Consultas SQL às tabelas ``conversas_orientacao`` e ``pedidos_llm`` (padrão Repository). Só este ficheiro tem SQL da orientação."""
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


def pedidos_no_dia(db: sqlite3.Connection, user_id: int, dia: str) -> int:
    linha = db.execute("SELECT total FROM pedidos_llm WHERE user_id = ? AND dia = ?", (user_id, dia)).fetchone()
    return linha["total"] if linha else 0


def contar_pedido(db: sqlite3.Connection, user_id: int, dia: str) -> None:
    db.execute(
        """
        INSERT INTO pedidos_llm (user_id, dia, total) VALUES (?, ?, 1)
        ON CONFLICT(user_id, dia) DO UPDATE SET total = total + 1
        """,
        (user_id, dia),
    )
    db.commit()


def pedidos_do_utilizador(db: sqlite3.Connection, user_id: int) -> list[sqlite3.Row]:
    """Pedidos ao LLM por dia, do mais antigo para o mais recente (exportar os meus dados, US46)."""
    return db.execute("SELECT dia, total FROM pedidos_llm WHERE user_id = ? ORDER BY dia", (user_id,)).fetchall()
