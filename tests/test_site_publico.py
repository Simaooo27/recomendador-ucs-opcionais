"""Site aberto a outras pessoas pelo túnel (revisão de 22/10): modo debug, ligação de confirmação
na página e limite de pedidos ao LLM por aluno e por dia. Sem rede (LLM falso)."""
from __future__ import annotations

import base64
import sqlite3
import unittest
import zlib
from unittest import mock

from app import create_app, texts
from app.llm.adaptadores import LLMFalso
from app.orientacao import limite
from tests.base import AppTestCase
from tests.test_conversa import ConversaTestCase, pergunta


class ModoDebugTests(unittest.TestCase):
    def test_recusa_arrancar_com_debug_num_site_publico(self):
        with mock.patch.dict("os.environ", {"FLASK_DEBUG": "1"}):
            with self.assertRaises(RuntimeError) as erro:
                create_app({"SECRET_KEY": "x", "DATABASE": ":memory:", "SESSION_COOKIE_SECURE": True})
        self.assertIn("--debug", str(erro.exception))

    def test_debug_em_desenvolvimento_continua_a_funcionar(self):
        with mock.patch.dict("os.environ", {"FLASK_DEBUG": "1"}):
            app = create_app({"SECRET_KEY": "x", "DATABASE": ":memory:", "SESSION_COOKIE_SECURE": False})
        self.assertTrue(app.debug)

    def test_site_publico_sem_debug_arranca(self):
        with mock.patch.dict("os.environ", {"FLASK_DEBUG": "0"}):
            app = create_app({"SECRET_KEY": "x", "DATABASE": ":memory:", "SESSION_COOKIE_SECURE": True})
        self.assertFalse(app.debug)


def _conteudo_do_cookie_de_sessao(client) -> str:
    """O que o navegador consegue ler no cookie de sessão (assinado, mas não cifrado)."""
    cookie = client.get_cookie("session")
    if cookie is None:
        return ""
    dados = cookie.value
    comprimido = dados.startswith(".")
    corpo = dados.lstrip(".").split(".")[0]
    corpo += "=" * (-len(corpo) % 4)
    bruto = base64.urlsafe_b64decode(corpo)
    return (zlib.decompress(bruto) if comprimido else bruto).decode("utf-8", "replace")


class LigacaoDeConfirmacaoVisivelTests(AppTestCase):
    def test_em_desenvolvimento_a_ligacao_aparece_na_pagina(self):
        self.register()
        html = self.client.get("/auth/registo/pendente").get_data(as_text=True)
        self.assertIn("/auth/confirmar/", html)


class LigacaoDeConfirmacaoEscondidaTests(AppTestCase):
    config_overrides = {"SHOW_DEV_CONFIRMATION_LINK": False}

    def test_a_ligacao_nao_aparece_na_pagina(self):
        self.register()
        html = self.client.get("/auth/registo/pendente").get_data(as_text=True)
        self.assertNotIn("/auth/confirmar/", html)
        self.assertNotIn("alert-dev", html)

    def test_a_ligacao_nao_fica_no_cookie_de_sessao(self):
        self.register()
        self.assertNotIn("confirmar", _conteudo_do_cookie_de_sessao(self.client))

    def test_o_email_com_a_ligacao_continua_a_ser_enviado(self):
        self.register()
        self.assertIn("/auth/confirmar/", self.mailer.outbox[-1].body)


class LimitePorAlunoTests(ConversaTestCase):
    def setUp(self):
        super().setUp()
        self.app.config["ORIENTACAO_MAX_PEDIDOS_DIA"] = 2
        self.usar_llm(LLMFalso([pergunta("Primeira?"), pergunta("Segunda?"), pergunta("Terceira?")]))

    def pedidos_guardados(self) -> list[tuple]:
        ligacao = sqlite3.connect(self.db_path)
        try:
            return ligacao.execute("SELECT user_id, dia, total FROM pedidos_llm").fetchall()
        finally:
            ligacao.close()

    def test_acima_do_limite_nao_chama_o_llm_e_a_conversa_fica_guardada(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        self.assertEqual(len(self.llm.pedidos), 2)
        with self.assertLogs(self.app.logger, level="INFO"):
            self.post("/orientacao/responder", resposta="Também gosto de Gestão")
        self.assertEqual(len(self.llm.pedidos), 2)
        html = self.pagina()
        self.assertIn(texts.ORIENTACAO_ERRO_LIMITE_ALUNO, html)
        self.assertIn("Também gosto de Gestão", html)          # a resposta não se perde
        self.assertIn(texts.ORIENTACAO_TENTAR_DE_NOVO, html)

    def test_o_limite_reinicia_no_dia_seguinte(self):
        with mock.patch.object(limite, "hoje_utc", return_value="2026-10-22"):
            self.post("/orientacao/comecar")
            self.post("/orientacao/responder", resposta="Gosto de Informática")
            with self.assertLogs(self.app.logger, level="INFO"):
                self.post("/orientacao/responder", resposta="E de Gestão")
        with mock.patch.object(limite, "hoje_utc", return_value="2026-10-23"):
            self.post("/orientacao/tentar-de-novo")
        self.assertEqual(len(self.llm.pedidos), 3)
        self.assertIn("Terceira?", self.pagina())

    def test_cada_aluno_tem_o_seu_limite(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        self.create_active_user("outro@gmail.com")
        outro = self.app.test_client()
        self.login(outro, email="outro@gmail.com")
        self.post("/orientacao/comecar", client=outro)
        self.assertEqual(len(self.llm.pedidos), 3)
        self.assertEqual(sorted(total for _, _, total in self.pedidos_guardados()), [1, 2])

    def test_zero_desliga_o_limite(self):
        self.app.config["ORIENTACAO_MAX_PEDIDOS_DIA"] = 0
        self.post("/orientacao/comecar")
        for resposta in ("a", "b"):
            self.post("/orientacao/responder", resposta=resposta)
        self.assertEqual(len(self.llm.pedidos), 3)

    def test_abrir_a_pagina_nao_conta(self):
        for _ in range(3):
            self.pagina()
        self.assertEqual(self.pedidos_guardados(), [])


class LigacoesPeloTunelTests(AppTestCase):
    """Pelo túnel (SESSION_COOKIE_SECURE=true), as ligações completas usam o endereço público."""
    config_overrides = {"SESSION_COOKIE_SECURE": True}

    def test_ligacao_de_partilha_tem_o_endereco_do_tunel(self):
        from tests.base import CSRF_TOKEN
        self.create_active_user()
        # O cloudflared liga-se a http://localhost:5000 e indica o endereço público nestes cabeçalhos.
        pedido = {"base_url": "http://localhost:5000",
                  "headers": {"X-Forwarded-Proto": "https", "X-Forwarded-Host": "exemplo.trycloudflare.com"}}
        with self.client.session_transaction(**pedido) as sessao:
            sessao["csrf_token"] = CSRF_TOKEN
        self.client.post("/auth/entrar", data={"csrf_token": CSRF_TOKEN, "email": "aluno@gmail.com", "password": "palavra-passe-1"}, **pedido)
        import re
        token = re.search(r'name="csrf_token" value="([^"]+)"', self.client.get("/candidatura/", **pedido).get_data(as_text=True)).group(1)
        self.client.post("/candidatura/partilhar", data={"csrf_token": token}, **pedido)
        html = self.client.get("/candidatura/", **pedido).get_data(as_text=True)
        self.assertIn('value="https://exemplo.trycloudflare.com/candidatura/p/', html)
