"""US02 — iniciar e terminar sessão (critérios de aceitação 1 a 4 + segurança)."""
import sqlite3

from tests.base import CSRF_TOKEN, VALID_EMAIL, VALID_PASSWORD, AppTestCase


def _location(response) -> str:
    return response.headers.get("Location", "")


class LoginFormTests(AppTestCase):
    def test_formulario_mostra_campos_e_ligacao_para_criar_conta(self):
        response = self.client.get("/auth/entrar")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for name in ("email", "password", "csrf_token"):
            self.assertIn(f'name="{name}"', html)
        self.assertIn('href="/auth/registo"', html)

    def test_pagina_inicial_sem_sessao_vai_para_o_inicio_de_sessao(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(_location(response).endswith("/auth/entrar"))


class SuccessfulLoginTests(AppTestCase):
    """Critério 1: login com email e palavra-passe."""

    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()

    def test_login_com_credenciais_corretas_cria_sessao(self):
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(_location(response).endswith("/inicio"))
        with self.client.session_transaction() as session:
            self.assertEqual(session["user_id"], self.fetch_user()["id"])
        page = self.client.get("/inicio")
        self.assertEqual(page.status_code, 200)
        self.assertIn(VALID_EMAIL, page.get_data(as_text=True))

    def test_email_com_maiusculas_e_espacos_inicia_sessao(self):
        response = self.login(email="  " + VALID_EMAIL.upper() + " ")
        self.assertTrue(_location(response).endswith("/inicio"))

    def test_sessao_renovada_apos_login(self):
        with self.client.session_transaction() as session:
            session["valor_antigo"] = "fixacao"
        self.login()
        with self.client.session_transaction() as session:
            self.assertNotIn("valor_antigo", session)
            self.assertNotEqual(session.get("csrf_token"), CSRF_TOKEN)

    def test_com_sessao_iniciada_a_pagina_de_login_vai_para_o_inicio(self):
        self.login()
        self.assertTrue(_location(self.client.get("/auth/entrar")).endswith("/inicio"))
        self.assertTrue(_location(self.client.get("/")).endswith("/inicio"))

    def test_barra_do_topo_mostra_terminar_sessao(self):
        self.login()
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn('action="/auth/sair"', html)


class InactiveAccountTests(AppTestCase):
    def test_conta_inativa_nao_inicia_sessao(self):
        self.register()  # conta criada mas por confirmar
        response = self.login()
        self.assertEqual(response.status_code, 403)
        self.assertIn("confirmou o seu email", response.get_data(as_text=True))
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)

    def test_conta_inativa_com_palavra_passe_errada_mostra_mensagem_generica(self):
        self.register()
        response = self.login(password="errada-123")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("confirmou o seu email", response.get_data(as_text=True))


class FailedLoginTests(AppTestCase):
    """Critério 2: mensagem genérica em caso de erro."""

    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()

    def assert_generic_error(self, response):
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Email ou palavra-passe incorretos.", html)
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)

    def test_palavra_passe_errada_mostra_mensagem_generica(self):
        self.assert_generic_error(self.login(password="errada-123"))

    def test_email_inexistente_mostra_a_mesma_mensagem(self):
        self.assert_generic_error(self.login(email="ninguem@gmail.com"))

    def test_campos_vazios_mostram_a_mesma_mensagem(self):
        self.assert_generic_error(self.login(email="", password=""))

    def test_palavra_passe_nunca_devolvida(self):
        html = self.login(password="segredo-errado-9").get_data(as_text=True)
        self.assertIn(f'value="{VALID_EMAIL}"', html)
        self.assertNotIn("segredo-errado-9", html)


class LogoutTests(AppTestCase):
    """Critério 3: o logout termina a sessão."""

    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()
        self.login()

    def test_logout_termina_a_sessao(self):
        response = self.logout()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(_location(response).endswith("/auth/entrar"))
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)
        self.assertTrue(_location(self.client.get("/inicio")).endswith("/auth/entrar"))

    def test_logout_exige_token_csrf(self):
        response = self.client.post("/auth/sair", data={"csrf_token": "token-errado"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get("/inicio").status_code, 200)

    def test_logout_por_get_nao_e_permitido(self):
        self.assertEqual(self.client.get("/auth/sair").status_code, 405)


class PrivatePageTests(AppTestCase):
    """Critério 4: páginas privadas redirecionam para o login."""

    def test_pagina_privada_sem_sessao_redireciona_para_login(self):
        response = self.client.get("/inicio")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(_location(response).endswith("/auth/entrar"))

    def test_pagina_privada_com_sessao_abre(self):
        self.create_active_user()
        self.login()
        self.assertEqual(self.client.get("/inicio").status_code, 200)

    def test_sessao_de_conta_que_deixou_de_existir_e_terminada(self):
        self.create_active_user()
        self.login()
        connection = sqlite3.connect(self.db_path)
        connection.execute("DELETE FROM users")
        connection.commit()
        connection.close()
        self.assertTrue(_location(self.client.get("/inicio")).endswith("/auth/entrar"))


class LoginSecurityTests(AppTestCase):
    def test_login_sem_token_csrf_e_rejeitado(self):
        self.create_active_user()
        response = self.client.post("/auth/entrar", data={"email": VALID_EMAIL, "password": VALID_PASSWORD})
        self.assertEqual(response.status_code, 400)
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)
