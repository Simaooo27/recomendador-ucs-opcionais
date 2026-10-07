"""Comando de terminal para criar administradores (US03).

Serve sobretudo para o primeiro administrador, que tem de ser criado por quem instala a
aplicação. Os seguintes podem ser criados por um administrador na área de gestão.

    flask --app app create-admin            # pede o nome e a palavra-passe
"""
from __future__ import annotations

import click
from flask import Flask, current_app
from flask.cli import with_appcontext

from .. import texts
from ..db import get_db
from . import repository, services


@click.command("create-admin")
@click.option("--username", prompt=texts.CLI_ADMIN_USERNAME_PROMPT, help="Nome de utilizador do administrador.")
@click.password_option("--password", prompt=texts.CLI_ADMIN_PASSWORD_PROMPT,
                       confirmation_prompt=texts.CLI_ADMIN_PASSWORD_CONFIRM_PROMPT)
@with_appcontext
def create_admin_command(username: str, password: str) -> None:
    """Cria um administrador (conta própria, sem email)."""
    db = get_db()
    try:
        services.create_admin(db, username, password, password, current_app.config, created_by=None)
    except services.AdminRejected as rejected:
        raise click.ClickException(" ".join(rejected.errors.values())) from rejected
    click.echo(texts.CLI_ADMIN_CREATED.format(nome=services.normalize_username(username), endereco=current_app.config["ADMIN_URL_PREFIX"] + "/entrar"))


@click.command("list-admins")
@with_appcontext
def list_admins_command() -> None:
    """Mostra os nomes dos administradores."""
    names = [row["username"] for row in repository.list_all(get_db())]
    click.echo("\n".join(names) if names else texts.CLI_NO_ADMINS)


def init_app(app: Flask) -> None:
    app.cli.add_command(create_admin_command)
    app.cli.add_command(list_admins_command)
