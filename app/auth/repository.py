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
    password_hash: str,
    nonce: str,
    privacy_version: str,
    now: str,
) -> int:
    cursor = db.execute(
        """
        INSERT INTO users (email, password_hash, confirmation_nonce,
                           privacy_policy_version, privacy_accepted_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (email, password_hash, nonce, privacy_version, now, now),
    )
    return int(cursor.lastrowid)


def refresh_pending_user(
    db: sqlite3.Connection,
    *,
    user_id: int,
    password_hash: str,
    nonce: str,
    privacy_version: str,
    now: str,
) -> None:
    """Atualiza um registo ainda não confirmado (novo pedido com o mesmo email)."""
    db.execute(
        """
        UPDATE users
           SET password_hash = ?, confirmation_nonce = ?,
               privacy_policy_version = ?, privacy_accepted_at = ?
         WHERE id = ? AND is_active = 0
        """,
        (password_hash, nonce, privacy_version, now, user_id),
    )


def activate_user(db: sqlite3.Connection, user_id: int, now: str) -> None:
    db.execute("UPDATE users SET is_active = 1, confirmed_at = ? WHERE id = ?", (now, user_id))
