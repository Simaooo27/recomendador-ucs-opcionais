"""Nome no registo (23/10, decisão do PO): o OptaBem trata a pessoa pelo nome e não pelo email."""
import os
import sqlite3
import tempfile
import unittest

from app import create_app, texts
from app.auth.validators import nome_error, normalize_nome, primeiro_nome
from tests.base import CSRF_TOKEN, VALID_EMAIL, AppTestCase


class RegrasDoNomeTests(unittest.TestCase):
    def test_aceita_nomes_reais(self):
        for nome in ("Ana", "Duarte Eusébio", "Ana-Rita Sá", "Joana D'Almeida", "J. Silva", "Zoë Müller"):
            with self.subTest(nome=nome):
                self.assertIsNone(nome_error(normalize_nome(nome)))

    def test_rejeita_vazio_numeros_simbolos_e_nomes_muito_longos(self):
        self.assertEqual(nome_error(normalize_nome("   ")), texts.ERROR_NOME_REQUIRED)
        for nome in ("Ana2", "<script>", "ana@gmail.com", "---", "A" * 61):
            with self.subTest(nome=nome):
                self.assertIsNotNone(nome_error(normalize_nome(nome)))

    def test_junta_espacos_e_tira_o_primeiro_nome(self):
        self.assertEqual(normalize_nome("  Ana   Rita  Silva "), "Ana Rita Silva")
        self.assertEqual(primeiro_nome("Duarte Eusébio"), "Duarte")
        self.assertEqual(primeiro_nome(""), "")


class RegistoComNomeTests(AppTestCase):
    def test_o_nome_e_obrigatorio(self):
        response = self.register(nome="")
        self.assertEqual(response.status_code, 422)
        self.assertIn(texts.ERROR_NOME_REQUIRED, response.get_data(as_text=True))
        self.assertEqual(self.count_users(), 0)

    def test_um_erro_noutro_campo_nao_apaga_o_nome_escrito(self):
        html = self.register(password="curta").get_data(as_text=True)
        self.assertIn('value="Ana Silva"', html)

    def test_o_nome_fica_guardado_sem_espacos_a_mais_e_o_email_diz_ola(self):
        self.register(nome="  Ana   Silva ")
        self.assertEqual(self.fetch_user()["nome"], "Ana Silva")
        self.assertTrue(self.mailer.outbox[-1].body.startswith("Olá, Ana,"))


class TratadoPeloNomeTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.create_active_user()
        self.login()

    def test_a_barra_do_topo_mostra_o_nome_e_o_email(self):
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn('<strong class="topo-nome">Ana Silva</strong>', html)
        self.assertIn(VALID_EMAIL, html)

    def test_mudar_o_nome_em_a_minha_conta(self):
        self.set_csrf()
        response = self.client.post("/auth/conta/nome", data={"csrf_token": CSRF_TOKEN, "nome": "Beatriz Costa"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.fetch_user()["nome"], "Beatriz Costa")
        self.assertIn("<h1>Olá, Beatriz!</h1>", self.client.get("/inicio").get_data(as_text=True))

    def test_nome_invalido_em_a_minha_conta_nao_muda_nada(self):
        self.set_csrf()
        response = self.client.post("/auth/conta/nome", data={"csrf_token": CSRF_TOKEN, "nome": "123"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.fetch_user()["nome"], "Ana Silva")

    def test_conta_sem_nome_e_convidada_a_indica_lo(self):
        connection = sqlite3.connect(self.db_path)
        connection.execute("UPDATE users SET nome = ''")
        connection.commit()
        connection.close()
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(f"<h1>{texts.HOME_GREETING}</h1>", html)
        self.assertIn(texts.HOME_SEM_NOME, html)
        self.assertIn(texts.CONTA_NOME_SEM, self.client.get("/auth/conta").get_data(as_text=True))


class BaseDeDadosAntigaTests(unittest.TestCase):
    """Uma base de dados criada antes de 23/10 (sem a coluna «nome») continua a funcionar."""

    def test_a_coluna_nome_e_acrescentada_ao_arrancar_sem_perder_contas(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "antiga.sqlite3")
            connection = sqlite3.connect(caminho)
            connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL)")
            connection.execute("INSERT INTO users (email) VALUES ('antigo@gmail.com')")
            connection.commit()
            connection.close()

            create_app({"TESTING": True, "SECRET_KEY": "teste", "DATABASE": caminho, "LLM_BACKEND": "falso"})

            connection = sqlite3.connect(caminho)
            linha = connection.execute("SELECT email, nome FROM users").fetchone()
            connection.close()
            self.assertEqual(linha, ("antigo@gmail.com", ""))


if __name__ == "__main__":
    unittest.main()
