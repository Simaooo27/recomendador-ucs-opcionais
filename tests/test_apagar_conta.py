"""US17 (âmbito reduzido a 22/10): apagar a minha conta e todos os meus dados.

A exportação dos dados passou para o backlog (decisão do PO de 22/10).
"""
from __future__ import annotations

import sqlite3

from app import texts
from app.catalogo import repository as catalogo_repository
from app.config import default_config
from tests.base import CSRF_TOKEN, VALID_EMAIL, VALID_PASSWORD, AppTestCase

CHAVE = catalogo_repository.todos(default_config()["CATALOGO_CSV"])[0].chave


class ApagarContaTestCase(AppTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()
        self.login()
        self.user_id = self.fetch_user()["id"]

    def _apagar(self, password=VALID_PASSWORD, *, with_csrf=True):
        if with_csrf:
            self.set_csrf()
        dados = {"csrf_token": CSRF_TOKEN} if with_csrf else {}
        if password is not None:
            dados["password"] = password
        return self.client.post("/auth/conta/apagar", data=dados)

    def _contar(self, tabela: str) -> int:
        ligacao = sqlite3.connect(self.db_path)
        try:
            return ligacao.execute(f"SELECT COUNT(*) FROM {tabela} WHERE user_id = ?", (self.user_id,)).fetchone()[0]
        finally:
            ligacao.close()

    def _criar_dados(self) -> None:
        """Uma conversa, uma decisão e um pedido ao LLM, como os de um aluno real."""
        self.set_csrf()
        self.client.post("/orientacao/comecar", data={"csrf_token": CSRF_TOKEN})
        self.client.post(f"/percurso/escolher/{CHAVE}", data={"csrf_token": CSRF_TOKEN})
        self.client.post("/orientacao/comecar", data={"csrf_token": CSRF_TOKEN})   # a escolha apagou a conversa
        ligacao = sqlite3.connect(self.db_path)
        try:
            # Um dia passado fixo: o teste não pode depender da data em que corre (a 23/10 falhou
            # porque os pedidos do próprio dia passaram a ser outra linha).
            ligacao.execute("INSERT OR IGNORE INTO pedidos_llm (user_id, dia, total) VALUES (?, '2026-10-01', 3)", (self.user_id,))
            ligacao.commit()
        finally:
            ligacao.close()


class PaginaTests(ApagarContaTestCase):
    """A página explica o que se perde e pede a palavra-passe."""

    def test_o_inicio_tem_a_ligacao(self):
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn('href="/auth/conta/apagar"', html)
        self.assertIn(texts.HOME_CONTA_APAGAR, html)

    def test_a_pagina_explica_e_pede_a_palavra_passe(self):
        html = self.client.get("/auth/conta/apagar").get_data(as_text=True)
        for item in texts.APAGAR_ITENS:
            self.assertIn(item, html)
        self.assertIn('type="password"', html)
        self.assertIn('name="csrf_token"', html)

    def test_sem_sessao_vai_para_o_inicio_de_sessao(self):
        anonimo = self.app.test_client()
        response = anonimo.get("/auth/conta/apagar")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/auth/entrar"))


class ConfirmacaoTests(ApagarContaTestCase):
    """Critério: a ação de apagar pede confirmação."""

    def test_palavra_passe_errada_nao_apaga(self):
        response = self._apagar("palavra-errada-123")
        self.assertEqual(response.status_code, 422)
        self.assertIn(texts.APAGAR_ERRO_PASSWORD, response.get_data(as_text=True))
        self.assertIsNotNone(self.fetch_user())

    def test_sem_palavra_passe_nao_apaga(self):
        self.assertEqual(self._apagar(None).status_code, 422)
        self.assertIsNotNone(self.fetch_user())

    def test_sem_csrf_nao_apaga(self):
        self.assertEqual(self._apagar(with_csrf=False).status_code, 400)
        self.assertIsNotNone(self.fetch_user())

    def test_abrir_a_pagina_nao_apaga_nada(self):
        self.client.get("/auth/conta/apagar")
        self.assertIsNotNone(self.fetch_user())


class ApagarTudoTests(ApagarContaTestCase):
    """Critério: apagar remove a conta, a conversa, as decisões e os pedidos ao LLM."""

    def test_apaga_a_conta_e_todos_os_dados(self):
        self._criar_dados()
        self.assertEqual(self._contar("decisoes"), 1)
        self.assertEqual(self._contar("conversas_orientacao"), 1)
        # Pelo menos o dia fixo de _criar_dados; os pedidos de hoje juntam outra linha.
        self.assertGreaterEqual(self._contar("pedidos_llm"), 1)

        response = self._apagar()
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.fetch_user())
        for tabela in ("decisoes", "conversas_orientacao", "pedidos_llm"):
            with self.subTest(tabela=tabela):
                self.assertEqual(self._contar(tabela), 0)

    def test_termina_a_sessao_e_avisa(self):
        response = self._apagar()
        self.assertTrue(response.headers["Location"].endswith("/"))
        pagina = self.client.get("/").get_data(as_text=True)
        self.assertIn(texts.APAGAR_FEITO, pagina)
        self.assertEqual(self.client.get("/inicio").status_code, 302)   # já não há sessão

    def test_nao_toca_nos_dados_de_outros_alunos(self):
        outro_email = "outra@gmail.com"
        self.create_active_user(email=outro_email)
        self._apagar()
        self.assertIsNone(self.fetch_user())
        self.assertIsNotNone(self.fetch_user(outro_email))

    def test_o_email_pode_voltar_a_registar_se(self):
        self._apagar()
        anonimo = self.app.test_client()
        response = self.register(anonimo, email=VALID_EMAIL, password=VALID_PASSWORD, password_confirm=VALID_PASSWORD)
        self.assertEqual(response.status_code, 302)


class PoliticaDePrivacidadeTests(AppTestCase):
    def test_a_politica_explica_como_apagar_e_ja_nao_promete_exportar(self):
        html = self.client.get("/privacidade").get_data(as_text=True)
        self.assertIn("Apagar a minha conta", html)
        self.assertNotIn("exportação", html)
