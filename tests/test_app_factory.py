"""Configuração da aplicação."""
import os
import unittest
from unittest import mock

from app import create_app
from app.mailer import ConsoleMailer, create_mailer


class AppFactoryTests(unittest.TestCase):
    def test_sem_secret_key_a_aplicacao_nao_arranca(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SECRET_KEY", None)
            with self.assertRaises(RuntimeError):
                create_app({"TESTING": True})

    def test_dominios_lidos_do_ambiente(self):
        with mock.patch.dict(os.environ, {"ALLOWED_EMAIL_DOMAINS": "A.pt, b.pt"}):
            app = create_app({"TESTING": True, "SECRET_KEY": "x", "DATABASE": ":memory:"})
        self.assertEqual(app.config["ALLOWED_EMAIL_DOMAINS"], ["a.pt", "b.pt"])


class MailerFactoryTests(unittest.TestCase):
    def test_console_por_omissao(self):
        self.assertIsInstance(create_mailer({}), ConsoleMailer)

    def test_smtp_exige_servidor(self):
        with self.assertRaises(RuntimeError):
            create_mailer({"MAIL_BACKEND": "smtp", "MAIL_SERVER": ""})

    def test_backend_desconhecido(self):
        with self.assertRaises(RuntimeError):
            create_mailer({"MAIL_BACKEND": "pombo-correio"})
