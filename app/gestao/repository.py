"""Acesso à tabela ``admins``. Todas as consultas são parametrizadas."""
from __future__ import annotations

import sqlite3


def get_by_username(db: sqlite3.Connection, username: str) -> sqlite3.Row | None:
    return db.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()


def get_by_id(db: sqlite3.Connection, admin_id: int) -> sqlite3.Row | None:
    return db.execute("SELECT * FROM admins WHERE id = ?", (admin_id,)).fetchone()


def list_all(db: sqlite3.Connection) -> list[sqlite3.Row]:
    return db.execute("SELECT * FROM admins ORDER BY username").fetchall()


def count(db: sqlite3.Connection) -> int:
    return int(db.execute("SELECT COUNT(*) FROM admins").fetchone()[0])


def create(db: sqlite3.Connection, *, username: str, password_hash: str, now: str, created_by: str | None) -> int:
    cursor = db.execute(
        "INSERT INTO admins (username, password_hash, created_at, created_by) VALUES (?, ?, ?, ?)",
        (username, password_hash, now, created_by),
    )
    return int(cursor.lastrowid)


def delete(db: sqlite3.Connection, admin_id: int) -> None:
    db.execute("DELETE FROM admins WHERE id = ?", (admin_id,))


def set_last_login(db: sqlite3.Connection, admin_id: int, now: str) -> None:
    db.execute("UPDATE admins SET last_login_at = ? WHERE id = ?", (now, admin_id))
