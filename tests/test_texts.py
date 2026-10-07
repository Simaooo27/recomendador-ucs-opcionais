"""Textos da interface (app/texts.py): protegem contra enganos ao editar o ficheiro."""
import string
import unittest
from unittest import mock

from app import texts
from tests.base import AppTestCase

# Marcadores que a aplicação preenche. Se um deles desaparecer de um texto, a página
# ou o email ficam incompletos (por exemplo, o email sem a ligação de confirmação).
REQUIRED_PLACEHOLDERS = {
    "PAGE_TITLE_FORMAT": {"pagina", "aplicacao"},
    "HOME_GREETING": {"email"},
    "ADMIN_DASHBOARD_GREETING": {"nome"},
    "ADMIN_PASSWORD_HINT": {"minimo"},
    "ADMIN_CREATED": {"nome"},
    "ADMIN_REMOVED": {"nome"},
    "CLI_ADMIN_CREATED": {"nome", "endereco"},
    "REGISTER_EMAIL_HINT": {"dominios"},
    "REGISTER_PASSWORD_HINT": {"minimo"},
    "ERROR_EMAIL_DOMAIN": {"dominios"},
    "ERROR_PASSWORD_TOO_SHORT": {"minimo"},
    "ERROR_PASSWORD_TOO_LONG": {"maximo"},
    "CONFIRMATION_EMAIL_BODY": {"horas", "ligacao"},
    "PRIVACY_VERSION": {"versao"},
}


def _all_texts() -> dict[str, str]:
    """Todos os textos; os que são listas (ex.: ADMIN_UPCOMING) contam linha a linha."""
    result = {}
    for name, value in vars(texts).items():
        if not name.isupper():
            continue
        if isinstance(value, list):
            result.update({f"{name}[{i}]": item for i, item in enumerate(value)})
        else:
            result[name] = value
    return result


def _placeholders(text: str) -> set[str]:
    return {field for _, field, _, _ in string.Formatter().parse(text) if field}


class TextsFileTests(unittest.TestCase):
    def test_todos_os_textos_sao_texto(self):
        for name, value in _all_texts().items():
            with self.subTest(texto=name):
                self.assertIsInstance(value, str)

    def test_textos_principais_nao_estao_vazios(self):
        for name, value in _all_texts().items():
            if name.endswith(("_BEFORE_LINK", "_AFTER_LINK", "_TO_END")):
                continue  # podem ficar vazios de propósito
            with self.subTest(texto=name):
                self.assertTrue(value.strip())

    def test_marcadores_obrigatorios_estao_presentes(self):
        for name, required in REQUIRED_PLACEHOLDERS.items():
            with self.subTest(texto=name):
                self.assertEqual(_placeholders(getattr(texts, name)), required)

    def test_textos_sem_marcadores_nao_tem_chavetas(self):
        for name, value in _all_texts().items():
            if name in REQUIRED_PLACEHOLDERS:
                continue
            with self.subTest(texto=name):
                self.assertEqual(_placeholders(value), set())


class TextsInPagesTests(AppTestCase):
    def test_nome_da_aplicacao_aparece_no_topo_e_no_separador(self):
        with mock.patch.object(texts, "APP_NAME", "OptaBem"):
            html = self.client.get("/auth/registo").get_data(as_text=True)
        self.assertIn("<span>OptaBem</span>", html)
        self.assertIn("<title>Criar conta · OptaBem</title>", html)

    def test_titulo_da_pagina_vem_dos_textos(self):
        with mock.patch.object(texts, "REGISTER_TITLE", "Registo"):
            html = self.client.get("/auth/registo").get_data(as_text=True)
        self.assertIn("<h1>Registo</h1>", html)

    def test_email_de_confirmacao_usa_os_textos(self):
        with mock.patch.object(texts, "CONFIRMATION_EMAIL_SUBJECT", "Bem-vindo"):
            self.register()
        message = self.mailer.outbox[-1]
        self.assertEqual(message.subject, "Bem-vindo")
        self.assertIn("/auth/confirmar/", message.body)


class PasswordToggleTests(AppTestCase):
    """Ícone de olho para mostrar ou esconder a palavra-passe (registo e início de sessão)."""

    def test_registo_tem_o_icone_nos_dois_campos(self):
        html = self.client.get("/auth/registo").get_data(as_text=True)
        self.assertIn('data-toggle-password="password"', html)
        self.assertIn('data-toggle-password="password_confirm"', html)
        self.assertIn('aria-label="Mostrar palavra-passe"', html)

    def test_inicio_de_sessao_tem_o_icone(self):
        html = self.client.get("/auth/entrar").get_data(as_text=True)
        self.assertIn('data-toggle-password="password"', html)

    def test_o_script_e_um_ficheiro_proprio(self):
        # A política de segurança (CSP) não deixa correr scripts escritos dentro da página.
        html = self.client.get("/auth/entrar").get_data(as_text=True)
        self.assertIn('src="/static/password-toggle.js"', html)
        response = self.client.get("/static/password-toggle.js")
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_o_campo_continua_a_ser_de_palavra_passe(self):
        html = self.client.get("/auth/registo").get_data(as_text=True)
        self.assertIn('id="password" name="password" type="password"', html)
