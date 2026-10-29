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


# Colunas acrescentadas a tabelas que já existiam. ``CREATE TABLE IF NOT EXISTS`` não altera uma
# tabela já criada, por isso uma base de dados antiga recebe-as aqui (sem perder dados).
_COLUNAS_NOVAS = (
    ("users", "nome", "TEXT NOT NULL DEFAULT ''"),   # nome no registo (23/10)
    ("planos_candidatura", "partilha", "TEXT"),      # partilhar o plano (23/10); único: índice abaixo
    ("conversas_orientacao", "usar_notas", "INTEGER NOT NULL DEFAULT 0"),   # assistente com as notas (US37)
)


def migrar(connection: sqlite3.Connection) -> None:
    """Acrescenta as colunas de ``_COLUNAS_NOVAS`` que faltem. Seguro de executar várias vezes."""
    for tabela, coluna, definicao in _COLUNAS_NOVAS:
        existentes = {linha[1] for linha in connection.execute(f"PRAGMA table_info({tabela})")}
        if existentes and coluna not in existentes:
            connection.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")
    # SQLite não acrescenta colunas UNIQUE: o código da partilha fica único por um índice.
    if {linha[1] for linha in connection.execute("PRAGMA table_info(planos_candidatura)")}:
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS planos_por_partilha ON planos_candidatura (partilha)")
    connection.commit()


def init_db() -> None:
    """Cria as tabelas, se ainda não existirem, e acrescenta as colunas novas."""
    connection = get_db()
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    migrar(connection)


@click.command("init-db")
def init_db_command() -> None:
    """Cria as tabelas da base de dados."""
    init_db()
    click.echo("Base de dados inicializada.")


def init_app(app: Flask) -> None:
    caminho = Path(app.config["DATABASE"])
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if caminho.exists():
        # Uma base de dados criada antes de uma tabela ou coluna nova continua a funcionar sem
        # ter de correr «flask init-db» outra vez (o esquema só cria o que falta).
        connection = sqlite3.connect(caminho)
        try:
            connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            migrar(connection)
        finally:
            connection.close()
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
