"""US03 — administradores independentes e área de gestão escondida (critérios 1 a 5)."""
import sqlite3

from app import create_app
from app.db import init_db
from tests.base import CSRF_TOKEN, AppTestCase

ADMIN = "gestor"
ADMIN_PASSWORD = "gestao-segura-1"


class GestaoTestCase(AppTestCase):
    def cli_create(self, username=ADMIN, password=ADMIN_PASSWORD):
        runner = self.app.test_cli_runner()
        return runner.invoke(args=["create-admin", "--username", username, "--password", password])

    def admin_login(self, client=None, username=ADMIN, password=ADMIN_PASSWORD):
        client = client or self.client
        self.set_csrf(client)
        return client.post("/gestao/entrar", data={"csrf_token": CSRF_TOKEN, "username": username, "password": password})

    def post(self, url, **data):
        self.set_csrf()
        return self.client.post(url, data={"csrf_token": CSRF_TOKEN, **data})

    def admins_in_db(self):
        connection = sqlite3.connect(self.db_path)
        try:
            return [row[0] for row in connection.execute("SELECT username FROM admins ORDER BY username")]
        finally:
            connection.close()


class SeparateAccountsTests(GestaoTestCase):
    """Critério 1: os administradores têm contas próprias, sem email e separadas dos alunos."""

    def test_administrador_fica_na_tabela_admins_e_nao_em_users(self):
        self.cli_create()
        self.assertEqual(self.admins_in_db(), [ADMIN])
        self.assertEqual(self.count_users(), 0)

    def test_registo_publico_cria_sempre_alunos(self):
        self.register(role="admin", username="intruso")
        self.assertEqual(self.admins_in_db(), [])
        self.assertEqual(self.fetch_user()["role"], "aluno")

    def test_aluno_nao_entra_na_gestao_com_as_suas_credenciais(self):
        self.create_active_user()
        response = self.admin_login(username="aluno@gmail.com", password="palavra-passe-1")
        self.assertEqual(response.status_code, 401)

    def test_administrador_nao_entra_no_login_dos_alunos(self):
        self.cli_create()
        response = self.login(email=ADMIN, password=ADMIN_PASSWORD)
        self.assertEqual(response.status_code, 401)

    def test_palavra_passe_guardada_com_hash(self):
        self.cli_create()
        connection = sqlite3.connect(self.db_path)
        stored = connection.execute("SELECT password_hash FROM admins").fetchone()[0]
        connection.close()
        self.assertNotIn(ADMIN_PASSWORD, stored)
        self.assertTrue(stored.startswith("scrypt:"))


class FirstAdminCommandTests(GestaoTestCase):
    """Critério 2: o primeiro administrador é criado no terminal."""

    def test_cria_o_administrador(self):
        result = self.cli_create()
        self.assertEqual(result.exit_code, 0)
        self.assertIn("criado", result.output)
        self.assertIn("/gestao/entrar", result.output)

    def test_pede_o_nome_e_a_palavra_passe_quando_nao_sao_dados(self):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=["create-admin"], input=f"{ADMIN}\n{ADMIN_PASSWORD}\n{ADMIN_PASSWORD}\n")
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn(ADMIN_PASSWORD, result.output)  # a palavra-passe não aparece no ecrã
        self.assertEqual(self.admins_in_db(), [ADMIN])

    def test_rejeita_palavra_passe_fraca(self):
        result = self.cli_create(password="abc")
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(self.admins_in_db(), [])

    def test_rejeita_nome_repetido_sem_distinguir_maiusculas(self):
        self.cli_create()
        result = self.cli_create(username="GESTOR")
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Já existe", result.output)

    def test_list_admins(self):
        runner = self.app.test_cli_runner()
        self.assertIn("Ainda não há administradores", runner.invoke(args=["list-admins"]).output)
        self.cli_create()
        self.assertIn(ADMIN, runner.invoke(args=["list-admins"]).output)


class AdminLoginTests(GestaoTestCase):
    """Critério 3: a gestão tem início de sessão próprio, com mensagem genérica."""

    def setUp(self) -> None:
        super().setUp()
        self.cli_create()

    def test_entra_com_nome_e_palavra_passe(self):
        response = self.admin_login()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/gestao/"))
        self.assertIn("Painel de gestão", self.client.get("/gestao/").get_data(as_text=True))

    def test_nome_com_maiusculas_e_espacos(self):
        self.assertEqual(self.admin_login(username="  Gestor ").status_code, 302)

    def test_credenciais_erradas_mostram_mensagem_generica(self):
        for username, password in ((ADMIN, "errada-123"), ("ninguem", ADMIN_PASSWORD)):
            with self.subTest(username=username):
                response = self.admin_login(username=username, password=password)
                self.assertEqual(response.status_code, 401)
                self.assertIn("Nome de utilizador ou palavra-passe incorretos.", response.get_data(as_text=True))

    def test_regista_a_ultima_entrada(self):
        self.admin_login()
        connection = sqlite3.connect(self.db_path)
        last = connection.execute("SELECT last_login_at FROM admins").fetchone()[0]
        connection.close()
        self.assertTrue(last)

    def test_terminar_sessao(self):
        self.admin_login()
        response = self.post("/gestao/sair")
        self.assertTrue(response.headers["Location"].endswith("/gestao/entrar"))
        self.assertTrue(self.client.get("/gestao/").headers["Location"].endswith("/gestao/entrar"))

    def test_login_sem_token_csrf_e_rejeitado(self):
        response = self.client.post("/gestao/entrar", data={"username": ADMIN, "password": ADMIN_PASSWORD})
        self.assertEqual(response.status_code, 400)


class HiddenAreaTests(GestaoTestCase):
    """Critério 4: a área de gestão está escondida dos alunos."""

    def test_nenhuma_pagina_dos_alunos_tem_ligacao_para_a_gestao(self):
        self.create_active_user()
        pages = ["/auth/entrar", "/auth/registo", "/privacidade"]
        html = "".join(self.client.get(page).get_data(as_text=True) for page in pages)
        self.login()
        html += self.client.get("/inicio").get_data(as_text=True)
        self.assertNotIn("/gestao", html)
        self.assertNotIn("Gestão", html)

    def test_paginas_da_gestao_sem_sessao_vao_para_o_login_da_gestao(self):
        for url in ("/gestao/", "/gestao/administradores"):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.headers["Location"].endswith("/gestao/entrar"))

    def test_sessao_de_aluno_nao_da_acesso_a_gestao(self):
        self.create_active_user()
        self.login()
        self.assertTrue(self.client.get("/gestao/").headers["Location"].endswith("/gestao/entrar"))

    def test_paginas_da_gestao_pedem_para_nao_ser_indexadas(self):
        html = self.client.get("/gestao/entrar").get_data(as_text=True)
        self.assertIn('<meta name="robots" content="noindex, nofollow">', html)
        self.assertNotIn("noindex", self.client.get("/auth/entrar").get_data(as_text=True))

    def test_endereco_da_gestao_e_configuravel(self):
        app = create_app({"TESTING": True, "SECRET_KEY": "x", "DATABASE": self.db_path, "ADMIN_URL_PREFIX": "/painel-interno"})
        with app.app_context():
            init_db()
        client = app.test_client()
        self.assertEqual(client.get("/painel-interno/entrar").status_code, 200)
        self.assertEqual(client.get("/gestao/entrar").status_code, 404)


class ManageAdminsTests(GestaoTestCase):
    """Critério 5: um administrador cria e remove outros administradores na área de gestão."""

    def setUp(self) -> None:
        super().setUp()
        self.cli_create()
        self.admin_login()

    def test_lista_mostra_quem_criou_cada_administrador(self):
        self.post("/gestao/administradores", username="ana.gestora", password="outra-senha-2", password_confirm="outra-senha-2")
        html = self.client.get("/gestao/administradores").get_data(as_text=True)
        self.assertIn("ana.gestora", html)
        self.assertIn("terminal", html)  # o primeiro foi criado no terminal

    def test_cria_outro_administrador(self):
        response = self.post("/gestao/administradores", username="ana.gestora", password="outra-senha-2", password_confirm="outra-senha-2")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.admins_in_db(), ["ana.gestora", ADMIN])
        other = self.app.test_client()
        self.assertEqual(self.admin_login(other, "ana.gestora", "outra-senha-2").status_code, 302)

    def test_dados_invalidos_mostram_os_erros(self):
        response = self.post("/gestao/administradores", username="A B", password="curta", password_confirm="x")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 422)
        self.assertIn('id="username-error"', html)
        self.assertIn('id="password-error"', html)
        self.assertNotIn("curta", html)
        self.assertEqual(self.admins_in_db(), [ADMIN])

    def test_nome_repetido_e_rejeitado(self):
        response = self.post("/gestao/administradores", username=ADMIN, password="outra-senha-2", password_confirm="outra-senha-2")
        self.assertEqual(response.status_code, 422)

    def test_remove_outro_administrador_e_a_sessao_dele_termina(self):
        self.post("/gestao/administradores", username="ana.gestora", password="outra-senha-2", password_confirm="outra-senha-2")
        other = self.app.test_client()
        self.admin_login(other, "ana.gestora", "outra-senha-2")
        connection = sqlite3.connect(self.db_path)
        ana_id = connection.execute("SELECT id FROM admins WHERE username = 'ana.gestora'").fetchone()[0]
        connection.close()
        self.post(f"/gestao/administradores/{ana_id}/remover")
        self.assertEqual(self.admins_in_db(), [ADMIN])
        self.assertTrue(other.get("/gestao/").headers["Location"].endswith("/gestao/entrar"))

    def test_quem_criou_continua_registado_depois_de_ser_removido(self):
        self.post("/gestao/administradores", username="ana.gestora", password="outra-senha-2", password_confirm="outra-senha-2")
        other = self.app.test_client()
        self.admin_login(other, "ana.gestora", "outra-senha-2")
        self.set_csrf(other)
        other.post("/gestao/administradores", data={"csrf_token": CSRF_TOKEN, "username": "rui.gestor", "password": "mais-uma-3", "password_confirm": "mais-uma-3"})
        connection = sqlite3.connect(self.db_path)
        ana_id = connection.execute("SELECT id FROM admins WHERE username = 'ana.gestora'").fetchone()[0]
        connection.close()
        self.post(f"/gestao/administradores/{ana_id}/remover")
        html = self.client.get("/gestao/administradores").get_data(as_text=True)
        row = html[html.index("rui.gestor"):html.index("</tr>", html.index("rui.gestor"))]
        self.assertIn("ana.gestora", row)

    def test_nao_pode_remover_a_propria_conta(self):
        connection = sqlite3.connect(self.db_path)
        own_id = connection.execute("SELECT id FROM admins").fetchone()[0]
        connection.close()
        self.post(f"/gestao/administradores/{own_id}/remover")
        self.assertEqual(self.admins_in_db(), [ADMIN])
        self.assertIn("Não pode remover a sua própria conta", self.client.get("/gestao/administradores").get_data(as_text=True))

    def test_criar_sem_token_csrf_e_rejeitado(self):
        response = self.client.post("/gestao/administradores", data={"username": "x.y", "password": "outra-senha-2", "password_confirm": "outra-senha-2"})
        self.assertEqual(response.status_code, 400)
