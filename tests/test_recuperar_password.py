"""US47: recuperar a palavra-passe com uma ligação enviada por email."""
from __future__ import annotations

import re
import time
from unittest import mock

from app import texts
from tests.base import CSRF_TOKEN, VALID_EMAIL, VALID_PASSWORD, AppTestCase

NOVA = "palavra-nova-42"
_LIGACAO = re.compile(r"/auth/recuperar/([A-Za-z0-9_\-.]+)")


class RecuperarTestCase(AppTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()

    def _pedir(self, email=VALID_EMAIL, client=None):
        client = client or self.client
        self.set_csrf(client)
        return client.post("/auth/recuperar", data={"csrf_token": CSRF_TOKEN, "email": email})

    def _token(self) -> str:
        match = _LIGACAO.search(self.mailer.outbox[-1].body)
        self.assertIsNotNone(match, "O email não tem a ligação de recuperação")
        return match.group(1)

    def _mudar(self, token, password=NOVA, confirm=None, client=None):
        client = client or self.client
        self.set_csrf(client)
        dados = {"csrf_token": CSRF_TOKEN, "password": password, "password_confirm": NOVA if confirm is None else confirm}
        return client.post(f"/auth/recuperar/{token}", data=dados)


class PedidoTests(RecuperarTestCase):
    """Critério: a mensagem é a mesma quer a conta exista quer não."""

    def test_o_inicio_de_sessao_tem_a_ligacao(self):
        html = self.client.get("/auth/entrar").get_data(as_text=True)
        self.assertIn('href="/auth/recuperar"', html)
        self.assertIn(texts.LOGIN_FORGOT, html)

    def test_conta_existente_recebe_o_email_com_a_ligacao(self):
        antes = len(self.mailer.outbox)
        response = self._pedir()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/auth/recuperar/enviado"))
        self.assertEqual(len(self.mailer.outbox), antes + 1)
        self.assertEqual(self.mailer.outbox[-1].to, VALID_EMAIL)
        self.assertEqual(self.mailer.outbox[-1].subject, texts.RECUPERAR_EMAIL_SUBJECT)
        self._token()

    def test_a_resposta_e_igual_com_e_sem_conta(self):
        com_conta = self._pedir()
        antes = len(self.mailer.outbox)
        sem_conta = self._pedir("ninguem@gmail.com", client=self.app.test_client())
        self.assertEqual(len(self.mailer.outbox), antes)   # não envia nada
        self.assertEqual((com_conta.status_code, com_conta.headers["Location"]), (sem_conta.status_code, sem_conta.headers["Location"]))
        pagina = self.client.get("/auth/recuperar/enviado").get_data(as_text=True)
        self.assertIn(texts.RECUPERAR_ENVIADO, pagina)
        self.assertNotIn(VALID_EMAIL, pagina)

    def test_maiusculas_e_espacos_no_email_tambem_servem(self):
        self._pedir("  " + VALID_EMAIL.upper() + " ")
        self.assertEqual(self.mailer.outbox[-1].to, VALID_EMAIL)

    def test_conta_por_confirmar_nao_recebe_ligacao(self):
        self.register(self.app.test_client(), email="pendente@gmail.com")
        antes = len(self.mailer.outbox)
        response = self._pedir("pendente@gmail.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.mailer.outbox), antes)

    def test_email_mal_escrito_e_assinalado(self):
        response = self._pedir("nao-e-um-email")
        self.assertEqual(response.status_code, 422)
        self.assertIn(texts.ERROR_EMAIL_INVALID, response.get_data(as_text=True))

    def test_a_ligacao_nunca_aparece_na_pagina(self):
        """Ao contrário da confirmação em desenvolvimento: senão, qualquer pessoa mudava a palavra-passe de outra."""
        self._pedir()
        token = self._token()
        pagina = self.client.get("/auth/recuperar/enviado").get_data(as_text=True)
        self.assertNotIn(token, pagina)
        with self.client.session_transaction() as sessao:
            self.assertNotIn(token, str(dict(sessao)))

    def test_falha_no_envio_nao_revela_que_a_conta_existe(self):
        with mock.patch.object(self.mailer, "send", side_effect=OSError("sem rede")), self.assertLogs(self.app.logger, "ERROR"):
            response = self._pedir()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/auth/recuperar/enviado"))

    def test_sem_csrf_e_recusado(self):
        response = self.client.post("/auth/recuperar", data={"email": VALID_EMAIL})
        self.assertEqual(response.status_code, 400)


class LigacaoTests(RecuperarTestCase):
    """Critério: ligação de uso único, que expira ao fim de 1 hora."""

    def setUp(self) -> None:
        super().setUp()
        self._pedir()
        self.token = self._token()

    def test_a_ligacao_abre_o_formulario_sem_cache(self):
        response = self.client.get(f"/auth/recuperar/{self.token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(texts.RECUPERAR_NOVA_TITLE, response.get_data(as_text=True))
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")

    def test_muda_a_palavra_passe(self):
        response = self._mudar(self.token)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/auth/entrar"))
        self.assertIn(texts.RECUPERAR_FEITO, self.client.get("/auth/entrar").get_data(as_text=True))
        self.assertEqual(self.login(self.app.test_client(), password=VALID_PASSWORD).status_code, 401)
        self.assertEqual(self.login(self.app.test_client(), password=NOVA).status_code, 302)

    def test_a_ligacao_so_serve_uma_vez(self):
        self._mudar(self.token)
        self.assertEqual(self.client.get(f"/auth/recuperar/{self.token}").status_code, 400)
        response = self._mudar(self.token, password="outra-vez-77", confirm="outra-vez-77")
        self.assertEqual(response.status_code, 400)
        self.assertIn(texts.RECUPERAR_INVALIDA, response.get_data(as_text=True))
        self.assertEqual(self.login(self.app.test_client(), password=NOVA).status_code, 302)

    def test_pedir_outra_ligacao_nao_invalida_a_primeira_enquanto_nao_for_usada(self):
        """Duas ligações pedidas seguidas servem as duas, mas só até uma ser usada."""
        self._pedir()
        segunda = self._token()
        self.assertEqual(self._mudar(segunda).status_code, 302)
        self.assertEqual(self.client.get(f"/auth/recuperar/{self.token}").status_code, 400)

    def test_expira_ao_fim_de_1_hora(self):
        self.assertEqual(self.app.config["RESET_TOKEN_MAX_AGE_SECONDS"], 3600)
        depois = time.time() + 3601
        with mock.patch("itsdangerous.timed.time.time", return_value=depois):
            pagina = self.client.get(f"/auth/recuperar/{self.token}")
            mudar = self._mudar(self.token)
        self.assertEqual(pagina.status_code, 410)
        self.assertIn(texts.RECUPERAR_EXPIRADA, pagina.get_data(as_text=True))
        self.assertEqual(mudar.status_code, 410)
        self.assertEqual(self.login(self.app.test_client(), password=VALID_PASSWORD).status_code, 302)

    def test_antes_de_1_hora_ainda_serve(self):
        quase = time.time() + 3500
        with mock.patch("itsdangerous.timed.time.time", return_value=quase):
            self.assertEqual(self.client.get(f"/auth/recuperar/{self.token}").status_code, 200)

    def test_ligacao_adulterada_nao_serve(self):
        self.assertEqual(self.client.get(f"/auth/recuperar/{self.token}x").status_code, 400)
        self.assertEqual(self.client.get("/auth/recuperar/nada").status_code, 400)

    def test_o_token_de_confirmacao_nao_serve_para_recuperar(self):
        """Os dois tokens são assinados com «sal» diferente."""
        self.register(self.app.test_client(), email="outra@gmail.com")
        confirmacao = self.last_token()
        self.assertEqual(self.client.get(f"/auth/recuperar/{confirmacao}").status_code, 400)

    def test_a_palavra_passe_nova_segue_as_regras_do_registo(self):
        for nova, confirm, campo in (("curta1", "curta1", "password"), ("semnumeros", "semnumeros", "password"), (NOVA, "diferente-1", "password_confirm")):
            with self.subTest(nova=nova):
                response = self._mudar(self.token, password=nova, confirm=confirm)
                self.assertEqual(response.status_code, 422)
                self.assertIn(f'id="{campo}-error"', response.get_data(as_text=True))
        # A ligação continua a servir depois de um erro: a palavra-passe não mudou.
        self.assertEqual(self._mudar(self.token).status_code, 302)

    def test_sem_csrf_e_recusado(self):
        response = self.client.post(f"/auth/recuperar/{self.token}", data={"password": NOVA, "password_confirm": NOVA})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.login(self.app.test_client(), password=VALID_PASSWORD).status_code, 302)


class SessoesTests(RecuperarTestCase):
    """Critério: depois de mudar a palavra-passe, as sessões abertas terminam."""

    def test_as_sessoes_abertas_noutros_dispositivos_terminam(self):
        portatil, telemovel = self.app.test_client(), self.app.test_client()
        self.login(portatil)
        self.login(telemovel)
        self.assertEqual(portatil.get("/inicio").status_code, 200)
        self._pedir()
        self._mudar(self._token())
        for cliente in (portatil, telemovel):
            response = cliente.get("/inicio")
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.headers["Location"].endswith("/auth/entrar"))

    def test_a_sessao_do_proprio_navegador_tambem_termina(self):
        self.login()
        self._pedir()
        self._mudar(self._token())
        self.assertEqual(self.client.get("/inicio").status_code, 302)

    def test_as_sessoes_de_outras_contas_continuam(self):
        self.create_active_user(email="outra@gmail.com")
        outra = self.app.test_client()
        self.login(outra, email="outra@gmail.com")
        self._pedir()
        self._mudar(self._token())
        self.assertEqual(outra.get("/inicio").status_code, 200)

    def test_a_sessao_nao_guarda_o_hash_da_palavra_passe(self):
        self.login()
        with self.client.session_transaction() as sessao:
            self.assertNotIn(self.fetch_user()["password_hash"], str(dict(sessao)))
