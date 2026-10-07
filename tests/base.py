"""Base comum dos testes: aplicação com base de dados temporária e email simulado."""
from __future__ import annotations

import os
import re
import sqlite3
import tempfile
import unittest

from app import create_app
from app.db import init_db

CSRF_TOKEN = "token-csrf-de-teste"
VALID_EMAIL = "aluno@iscap.ipp.pt"
VALID_PASSWORD = "palavra-passe-1"
_TOKEN_IN_LINK = re.compile(r"/auth/confirmar/([A-Za-z0-9_\-.]+)")


class AppTestCase(unittest.TestCase):
    config_overrides: dict = {}

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self._tmp.name, "teste.sqlite3")
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "chave-so-para-testes",
                "DATABASE": self.db_path,
                "MAIL_CONSOLE_ECHO": False,
                **self.config_overrides,
            }
        )
        with self.app.app_context():
            init_db()
        self.client = self.app.test_client()
        self.mailer = self.app.extensions["mailer"]

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # -- auxiliares ---------------------------------------------------------
    def set_csrf(self, client=None) -> str:
        client = client or self.client
        with client.session_transaction() as session:
            session["csrf_token"] = CSRF_TOKEN
        return CSRF_TOKEN

    def register(self, client=None, *, with_csrf: bool = True, **overrides):
        """Submete o formulário de registo; por omissão com dados válidos."""
        client = client or self.client
        if with_csrf:
            self.set_csrf(client)
        data = {
            "csrf_token": CSRF_TOKEN,
            "email": VALID_EMAIL,
            "password": VALID_PASSWORD,
            "password_confirm": VALID_PASSWORD,
            "accepted_privacy": "on",
        }
        data.update(overrides)
        data = {key: value for key, value in data.items() if value is not None}
        return client.post("/auth/registo", data=data)

    def fetch_user(self, email: str = VALID_EMAIL):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            return connection.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        finally:
            connection.close()

    def count_users(self) -> int:
        connection = sqlite3.connect(self.db_path)
        try:
            return connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        finally:
            connection.close()

    def create_active_user(self, email: str = VALID_EMAIL, password: str = VALID_PASSWORD) -> None:
        """Regista e confirma uma conta, num cliente à parte (não deixa sessão no ``self.client``)."""
        other = self.app.test_client()
        response = self.register(other, email=email, password=password, password_confirm=password)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(other.get(f"/auth/confirmar/{self.last_token()}").status_code, 200)

    def login(self, client=None, *, with_csrf: bool = True, **overrides):
        """Submete o formulário de início de sessão; por omissão com dados válidos."""
        client = client or self.client
        if with_csrf:
            self.set_csrf(client)
        data = {"csrf_token": CSRF_TOKEN, "email": VALID_EMAIL, "password": VALID_PASSWORD}
        data.update(overrides)
        data = {key: value for key, value in data.items() if value is not None}
        return client.post("/auth/entrar", data=data)

    def logout(self, client=None, *, with_csrf: bool = True):
        client = client or self.client
        data = {"csrf_token": CSRF_TOKEN} if with_csrf else {}
        if with_csrf:
            self.set_csrf(client)
        return client.post("/auth/sair", data=data)

    def last_token(self) -> str:
        match = _TOKEN_IN_LINK.search(self.mailer.outbox[-1].body)
        self.assertIsNotNone(match, "O email não contém a ligação de confirmação")
        return match.group(1)
