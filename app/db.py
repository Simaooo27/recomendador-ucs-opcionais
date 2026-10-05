"""Acesso à base de dados SQLite (biblioteca padrão, sem ORM)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def get_db() -> sqlite3.Connection:
    """Devolve a ligação do pedido atual (criada à primeira utilização)."""
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(_exception: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    """Cria as tabelas, se ainda não existirem."""
    connection = get_db()
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    connection.commit()


@click.command("init-db")
def init_db_command() -> None:
    """Cria as tabelas da base de dados."""
    init_db()
    click.echo("Base de dados inicializada.")


def init_app(app: Flask) -> None:
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
