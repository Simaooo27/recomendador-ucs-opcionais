"""Um só início de sessão para alunos e administradores (US03, revisão de 14/10).

Padrões de desenho (ver docs/geral/03-arquitetura-e-padroes.md, secção 3):

- **Strategy** — cada perfil (``PerfilAluno``, ``PerfilAdministrador``) sabe, à sua maneira,
  reconhecer quem é dele, verificar a palavra-passe, abrir a sessão e qual é a sua página inicial.
  A rota de início de sessão não sabe que perfis existem.
- **Chain of Responsibility** — ``CadeiaDePerfis`` passa o pedido a cada perfil, por ordem, até um
  dizer «é comigo». Acrescentar um perfil novo não mexe nos outros nem na rota.
- **Factory** — ``criar_cadeia_de_perfis()`` monta a cadeia num só sítio; é aí que se acrescenta
  um perfil.

As contas continuam separadas (tabela ``users`` para alunos, tabela ``admins`` para
administradores) e a área de gestão continua sem ligações nas páginas dos alunos.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Protocol

from ..gestao import services as gestao_services
from ..gestao import sessions as gestao_sessions
from . import services, sessions
from .services import LoginOutcome


@dataclass(frozen=True)
class Entrada:
    """Resultado de uma tentativa de início de sessão."""

    outcome: LoginOutcome
    conta_id: int | None = None
    perfil: "Perfil | None" = None


class Perfil(Protocol):
    """Interface comum a todos os perfis (Strategy)."""

    nome: str
    pagina_inicial: str  # endpoint Flask para onde vai depois de entrar

    def reconhece(self, identificador: str) -> bool:
        """Diz se o identificador escrito no formulário pertence a este perfil."""

    def autenticar(self, db: sqlite3.Connection, identificador: str, palavra_passe: str) -> Entrada:
        """Verifica as credenciais na tabela deste perfil."""

    def iniciar_sessao(self, conta_id: int) -> None:
        """Abre a sessão deste perfil (começa sempre uma sessão nova)."""


class PerfilAluno:
    """Alunos: entram com o email (tabela ``users``)."""

    nome = "aluno"
    pagina_inicial = "main.home"

    def reconhece(self, identificador: str) -> bool:
        return "@" in identificador

    def autenticar(self, db: sqlite3.Connection, identificador: str, palavra_passe: str) -> Entrada:
        result = services.authenticate(db, identificador, palavra_passe)
        return Entrada(result.outcome, result.user_id, self)

    def iniciar_sessao(self, conta_id: int) -> None:
        sessions.login_user(conta_id)


class PerfilAdministrador:
    """Administradores: entram com o nome de utilizador (tabela ``admins``), que nunca tem «@»."""

    nome = "administrador"
    pagina_inicial = "gestao.dashboard"

    def reconhece(self, identificador: str) -> bool:
        return "@" not in identificador

    def autenticar(self, db: sqlite3.Connection, identificador: str, palavra_passe: str) -> Entrada:
        admin_id = gestao_services.authenticate(db, identificador, palavra_passe)
        if admin_id is None:
            return Entrada(LoginOutcome.INVALID_CREDENTIALS)
        return Entrada(LoginOutcome.SUCCESS, admin_id, self)

    def iniciar_sessao(self, conta_id: int) -> None:
        gestao_sessions.login_admin(conta_id)


class CadeiaDePerfis:
    """Passa o pedido a cada perfil até um o reconhecer (Chain of Responsibility)."""

    def __init__(self, perfis: list[Perfil]) -> None:
        self._perfis = perfis

    def entrar(self, db: sqlite3.Connection, identificador: str, palavra_passe: str) -> Entrada:
        identificador = identificador.strip()
        for perfil in self._perfis:
            if perfil.reconhece(identificador):
                return perfil.autenticar(db, identificador, palavra_passe)
        return Entrada(LoginOutcome.INVALID_CREDENTIALS)


def criar_cadeia_de_perfis() -> CadeiaDePerfis:
    """Factory: os perfis que podem iniciar sessão, pela ordem em que são consultados."""
    return CadeiaDePerfis([PerfilAluno(), PerfilAdministrador()])
