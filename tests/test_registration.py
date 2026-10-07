"""US01 — registo com email pessoal (critérios de aceitação 1, 3 e 4 + CSRF)."""
from werkzeug.security import check_password_hash

from tests.base import VALID_EMAIL, VALID_PASSWORD, AppTestCase


class RegistrationFormTests(AppTestCase):
    def test_formulario_mostra_campos_e_ligacao_a_politica(self):
        response = self.client.get("/auth/registo")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for name in ("email", "password", "password_confirm", "accepted_privacy", "csrf_token"):
            self.assertIn(f'name="{name}"', html)
        self.assertIn("/privacidade", html)
        self.assertNotIn("@iscap.ipp.pt", html)

    def test_formulario_tem_ligacao_para_iniciar_sessao(self):
        self.assertIn('href="/auth/entrar"', self.client.get("/auth/registo").get_data(as_text=True))

    def test_pagina_de_privacidade_existe(self):
        self.assertEqual(self.client.get("/privacidade").status_code, 200)


class SuccessfulRegistrationTests(AppTestCase):
    def test_regista_conta_inativa_e_redireciona(self):
        response = self.register()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/auth/registo/pendente"))
        user = self.fetch_user()
        self.assertIsNotNone(user)
        self.assertEqual(user["is_active"], 0)
        self.assertIsNone(user["confirmed_at"])
        self.assertEqual(user["role"], "aluno")

    def test_envia_um_email_com_ligacao_de_confirmacao(self):
        self.register()
        self.assertEqual(len(self.mailer.outbox), 1)
        message = self.mailer.outbox[0]
        self.assertEqual(message.to, VALID_EMAIL)
        self.assertIn("/auth/confirmar/", message.body)

    def test_pagina_pendente_mostra_o_email(self):
        self.register()
        html = self.client.get("/auth/registo/pendente").get_data(as_text=True)
        self.assertIn(VALID_EMAIL, html)

    def test_pagina_pendente_sem_sessao_nao_falha(self):
        self.assertEqual(self.client.get("/auth/registo/pendente").status_code, 200)

    def test_palavra_passe_guardada_com_hash(self):
        self.register()
        stored = self.fetch_user()["password_hash"]
        self.assertNotEqual(stored, VALID_PASSWORD)
        self.assertNotIn(VALID_PASSWORD, stored)
        self.assertTrue(check_password_hash(stored, VALID_PASSWORD))
        self.assertFalse(check_password_hash(stored, "outra-palavra-1"))

    def test_guarda_aceitacao_da_politica_com_versao_e_data(self):
        self.register()
        user = self.fetch_user()
        self.assertEqual(user["privacy_policy_version"], self.app.config["PRIVACY_POLICY_VERSION"])
        self.assertTrue(user["privacy_accepted_at"])

    def test_normaliza_o_email(self):
        self.register(email="  Aluno@GMAIL.com ")
        self.assertIsNotNone(self.fetch_user("aluno@gmail.com"))
        self.assertEqual(self.mailer.outbox[0].to, "aluno@gmail.com")

    def test_aceita_emails_de_varios_fornecedores(self):
        for email in ("nome@outlook.pt", "nome@sapo.pt", "nome@iscap.ipp.pt"):
            with self.subTest(email=email):
                self.assertEqual(self.register(email=email).status_code, 302)
                self.assertIsNotNone(self.fetch_user(email))


class RejectedRegistrationTests(AppTestCase):
    def assert_rejected(self, response, field: str):
        self.assertEqual(response.status_code, 422)
        self.assertIn(f'id="{field}-error"', response.get_data(as_text=True))
        self.assertEqual(self.count_users(), 0)
        self.assertEqual(self.mailer.outbox, [])

    def test_rejeita_email_mal_formado(self):
        self.assert_rejected(self.register(email="aluno@gmail"), "email")

    def test_rejeita_palavra_passe_fraca(self):
        self.assert_rejected(self.register(password="abc", password_confirm="abc"), "password")

    def test_rejeita_confirmacao_diferente(self):
        self.assert_rejected(self.register(password_confirm="diferente-123"), "password_confirm")

    def test_exige_aceitacao_da_politica_de_privacidade(self):
        self.assert_rejected(self.register(accepted_privacy=None), "accepted_privacy")

    def test_mantem_o_email_mas_nunca_devolve_a_palavra_passe(self):
        response = self.register(password="segredo-muito-1", password_confirm="outra-coisa-1")
        html = response.get_data(as_text=True)
        self.assertIn('value="aluno@gmail.com"', html)
        self.assertNotIn("segredo-muito-1", html)


class RestrictedDomainRegistrationTests(RejectedRegistrationTests):
    """Opção ALLOWED_EMAIL_DOMAINS: se a equipa voltar a exigir o email institucional."""

    config_overrides = {"ALLOWED_EMAIL_DOMAINS": ["iscap.ipp.pt"]}

    def register(self, client=None, **overrides):
        overrides.setdefault("email", "aluno@iscap.ipp.pt")
        return super().register(client, **overrides)

    def test_mantem_o_email_mas_nunca_devolve_a_palavra_passe(self):
        pass  # já coberto sem restrição

    def test_aceita_o_dominio_configurado_e_subdominios(self):
        for email in ("aluno@iscap.ipp.pt", "outro@alunos.iscap.ipp.pt"):
            with self.subTest(email=email):
                self.assertEqual(self.register(email=email).status_code, 302)

    def test_rejeita_email_fora_do_dominio(self):
        self.assert_rejected(self.register(email="aluno@gmail.com"), "email")

    def test_rejeita_dominio_parecido(self):
        self.assert_rejected(self.register(email="aluno@iscap.ipp.pt.evil.com"), "email")

    def test_formulario_e_erro_indicam_o_dominio_aceite(self):
        self.assertIn("@iscap.ipp.pt", self.client.get("/auth/registo").get_data(as_text=True))
        self.assertIn("@iscap.ipp.pt", self.register(email="aluno@gmail.com").get_data(as_text=True))


class DuplicateRegistrationTests(AppTestCase):
    def test_rejeita_email_de_conta_ja_ativa(self):
        self.register()
        self.client.get(f"/auth/confirmar/{self.last_token()}")
        response = self.register()
        self.assertEqual(response.status_code, 422)
        self.assertIn("Já existe uma conta", response.get_data(as_text=True))
        self.assertEqual(self.count_users(), 1)
        self.assertEqual(len(self.mailer.outbox), 1)

    def test_registo_repetido_de_conta_pendente_renova_e_reenvia(self):
        self.register()
        old_token = self.last_token()
        old_hash = self.fetch_user()["password_hash"]

        response = self.register(password="nova-palavra-2", password_confirm="nova-palavra-2")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.count_users(), 1)
        self.assertEqual(len(self.mailer.outbox), 2)
        self.assertNotEqual(self.fetch_user()["password_hash"], old_hash)
        self.assertNotEqual(self.last_token(), old_token)

    def test_ligacao_antiga_deixa_de_funcionar_apos_novo_registo(self):
        self.register()
        old_token = self.last_token()
        self.register()
        response = self.client.get(f"/auth/confirmar/{old_token}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.fetch_user()["is_active"], 0)

    def test_email_diferente_so_na_capitalizacao_conta_como_duplicado(self):
        self.register()
        self.register(email="ALUNO@gmail.com")
        self.assertEqual(self.count_users(), 1)


class EmailFailureTests(AppTestCase):
    def test_falha_no_envio_mostra_erro_e_nao_ativa_a_conta(self):
        class BrokenMailer:
            def send(self, message):
                raise OSError("SMTP indisponível")

        self.app.extensions["mailer"] = BrokenMailer()
        with self.assertLogs(self.app.logger, level="ERROR"):
            response = self.register()
        self.assertEqual(response.status_code, 503)
        self.assertIn("Não foi possível enviar o email", response.get_data(as_text=True))
        self.assertEqual(self.fetch_user()["is_active"], 0)


class CsrfTests(AppTestCase):
    def test_pedido_sem_token_e_rejeitado(self):
        response = self.register(csrf_token=None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.count_users(), 0)

    def test_pedido_com_token_errado_e_rejeitado(self):
        response = self.register(csrf_token="token-errado")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.count_users(), 0)

    def test_pedido_sem_sessao_e_rejeitado(self):
        response = self.register(with_csrf=False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.count_users(), 0)

    def test_token_do_formulario_e_aceite(self):
        html = self.client.get("/auth/registo").get_data(as_text=True)
        token = html.split('name="csrf_token" value="')[1].split('"')[0]
        response = self.register(with_csrf=False, csrf_token=token)
        self.assertEqual(response.status_code, 302)


class SecurityHeadersTests(AppTestCase):
    def test_cabecalhos_de_seguranca(self):
        response = self.client.get("/auth/registo")
        self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")


class DevConfirmationLinkTests(AppTestCase):
    """Em desenvolvimento (email no terminal), a ligação aparece também na página «Confirme o seu email»."""

    def test_em_desenvolvimento_a_pagina_mostra_a_ligacao(self):
        self.register()
        html = self.client.get("/auth/registo/pendente").get_data(as_text=True)
        self.assertIn(f"/auth/confirmar/{self.last_token()}", html)
        self.assertIn("Modo de desenvolvimento", html)

    def test_a_ligacao_da_pagina_ativa_a_conta(self):
        self.register()
        self.assertEqual(self.client.get(f"/auth/confirmar/{self.last_token()}").status_code, 200)
        self.assertEqual(self.fetch_user()["is_active"], 1)


class NoDevLinkWithRealEmailTests(AppTestCase):
    """Com email real (SMTP), a ligação nunca aparece na página."""

    config_overrides = {"MAIL_BACKEND": "smtp", "MAIL_SERVER": "smtp.exemplo.pt"}

    def setUp(self) -> None:
        super().setUp()
        from app.mailer import ConsoleMailer

        # Substitui o SMTP por um envio simulado, para o teste não usar a rede.
        self.mailer = self.app.extensions["mailer"] = ConsoleMailer(echo=False)

    def test_com_smtp_a_pagina_nao_mostra_a_ligacao(self):
        self.register()
        html = self.client.get("/auth/registo/pendente").get_data(as_text=True)
        self.assertNotIn("/auth/confirmar/", html)
        self.assertNotIn("Modo de desenvolvimento", html)
