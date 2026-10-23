"""Acesso à tabela ``users``. Todas as consultas são parametrizadas."""
from __future__ import annotations

import sqlite3


def get_by_email(db: sqlite3.Connection, email: str) -> sqlite3.Row | None:
    return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


def get_by_id(db: sqlite3.Connection, user_id: int) -> sqlite3.Row | None:
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def create_user(
    db: sqlite3.Connection,
    *,
    email: str,
    nome: str,
    password_hash: str,
    nonce: str,
    privacy_version: str,
    now: str,
) -> int:
    cursor = db.execute(
        """
        INSERT INTO users (email, nome, password_hash, confirmation_nonce,
                           privacy_policy_version, privacy_accepted_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (email, nome, password_hash, nonce, privacy_version, now, now),
    )
    return int(cursor.lastrowid)


def refresh_pending_user(
    db: sqlite3.Connection,
    *,
    user_id: int,
    nome: str,
    password_hash: str,
    nonce: str,
    privacy_version: str,
    now: str,
) -> None:
    """Atualiza um registo ainda não confirmado (novo pedido com o mesmo email)."""
    db.execute(
        """
        UPDATE users
           SET nome = ?, password_hash = ?, confirmation_nonce = ?,
               privacy_policy_version = ?, privacy_accepted_at = ?
         WHERE id = ? AND is_active = 0
        """,
        (nome, password_hash, nonce, privacy_version, now, user_id),
    )


def update_nome(db: sqlite3.Connection, user_id: int, nome: str) -> None:
    """Muda o nome da conta («A minha conta»)."""
    db.execute("UPDATE users SET nome = ? WHERE id = ?", (nome, user_id))
    db.commit()


def list_pending(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Contas por confirmar, da mais recente para a mais antiga (ativação pela gestão, 23/10)."""
    return db.execute(
        "SELECT id, nome, email, created_at FROM users WHERE is_active = 0 ORDER BY created_at DESC, id DESC"
    ).fetchall()


def activate_user(db: sqlite3.Connection, user_id: int, now: str) -> None:
    db.execute("UPDATE users SET is_active = 1, confirmed_at = ? WHERE id = ?", (now, user_id))


def count_by_status(db: sqlite3.Connection) -> tuple[int, int]:
    """Número de contas ativas e de contas por confirmar (painel de gestão)."""
    row = db.execute(
        "SELECT COALESCE(SUM(is_active), 0) AS ativas, COALESCE(SUM(1 - is_active), 0) AS pendentes FROM users"
    ).fetchone()
    return int(row["ativas"]), int(row["pendentes"])


def last_created_at(db: sqlite3.Connection) -> str | None:
    """Data do registo mais recente (UTC, ISO 8601), ou ``None`` se não houver contas."""
    return db.execute("SELECT MAX(created_at) AS ultimo FROM users").fetchone()["ultimo"]


def delete_user(db: sqlite3.Connection, user_id: int) -> None:
    """Apaga a conta (US17). A conversa, as decisões e os pedidos ao LLM saem com ela
    (``ON DELETE CASCADE`` em app/schema.sql; a ligação liga ``PRAGMA foreign_keys``)."""
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
