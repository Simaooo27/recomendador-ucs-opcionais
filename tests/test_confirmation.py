"""US01 — critério de aceitação 2: a conta só fica ativa após confirmação por email."""
from tests.base import AppTestCase


class ConfirmationTests(AppTestCase):
    def test_conta_nao_esta_ativa_antes_da_confirmacao(self):
        self.register()
        self.assertEqual(self.fetch_user()["is_active"], 0)

    def test_ligacao_valida_ativa_a_conta(self):
        self.register()
        response = self.client.get(f"/auth/confirmar/{self.last_token()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Conta ativada", response.get_data(as_text=True))
        user = self.fetch_user()
        self.assertEqual(user["is_active"], 1)
        self.assertTrue(user["confirmed_at"])

    def test_confirmacao_nao_deve_ser_guardada_em_cache(self):
        self.register()
        response = self.client.get(f"/auth/confirmar/{self.last_token()}")
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_ligacao_usada_duas_vezes_e_idempotente(self):
        self.register()
        token = self.last_token()
        self.client.get(f"/auth/confirmar/{token}")
        response = self.client.get(f"/auth/confirmar/{token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("já ativa", response.get_data(as_text=True))
        self.assertEqual(self.fetch_user()["is_active"], 1)

    def test_token_adulterado_e_rejeitado(self):
        self.register()
        response = self.client.get(f"/auth/confirmar/{self.last_token()}x")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.fetch_user()["is_active"], 0)

    def test_token_aleatorio_e_rejeitado(self):
        self.assertEqual(self.client.get("/auth/confirmar/isto-nao-e-um-token").status_code, 400)

    def test_token_assinado_com_outra_chave_e_rejeitado(self):
        from app.auth.tokens import make_confirmation_token

        self.register()
        forged = make_confirmation_token("outra-chave", self.fetch_user()["id"], "qualquer")
        self.assertEqual(self.client.get(f"/auth/confirmar/{forged}").status_code, 400)
        self.assertEqual(self.fetch_user()["is_active"], 0)

    def test_token_expirado_e_rejeitado(self):
        self.register()
        token = self.last_token()
        self.app.config["CONFIRMATION_TOKEN_MAX_AGE_SECONDS"] = -1  # tudo expira
        response = self.client.get(f"/auth/confirmar/{token}")
        self.assertEqual(response.status_code, 410)
        self.assertIn("expirada", response.get_data(as_text=True))
        self.assertEqual(self.fetch_user()["is_active"], 0)

    def test_token_de_utilizador_inexistente_e_rejeitado(self):
        import sqlite3

        self.register()
        token = self.last_token()
        connection = sqlite3.connect(self.db_path)
        connection.execute("DELETE FROM users")
        connection.commit()
        connection.close()
        self.assertEqual(self.client.get(f"/auth/confirmar/{token}").status_code, 400)

    def test_email_inclui_prazo_de_validade_em_horas(self):
        self.register()
        self.assertIn("24 horas", self.mailer.outbox[0].body)
