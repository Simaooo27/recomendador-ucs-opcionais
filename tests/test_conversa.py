"""US29 — Conversa de orientação com o LLM (/orientacao), com o LLM falso (sem rede)."""
from __future__ import annotations

import json
import sqlite3

from app import texts
from app.catalogo import repository as catalogo_repository
from app.config import default_config
from app.llm import LimiteAtingido, LLMIndisponivel
from app.llm.adaptadores import LLMFalso
from app.llm.decoradores import EMAIL_REMOVIDO, NUMERO_REMOVIDO, ProtegerDadosPessoais
from app.orientacao import conversa
from tests.base import CSRF_TOKEN, VALID_EMAIL, AppTestCase

CHAVE, CHAVE2 = (c.chave for c in catalogo_repository.todos(default_config()["CATALOGO_CSV"])[:2])


def pergunta(texto: str) -> str:
    return json.dumps({"tipo": "pergunta", "texto": texto})


def sugestao() -> str:
    cursos = [{"id": CHAVE, "explicacao": "x"}, {"id": CHAVE2, "explicacao": "y"}]
    return json.dumps({"tipo": "sugestao", "texto": "Tenho sugestões.", "cursos": cursos})


class LLMQueFalha:
    """Falha nas primeiras ``vezes`` chamadas e depois responde como o LLM falso."""

    nome = "falha"

    def __init__(self, erro: Exception, vezes: int, respostas: list[str]) -> None:
        self.erro, self.vezes, self.falso = erro, vezes, LLMFalso(respostas)

    def conversar(self, instrucoes, mensagens):
        if self.vezes > 0:
            self.vezes -= 1
            raise self.erro
        return self.falso.conversar(instrucoes, mensagens)


class ConversaTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.create_active_user()
        self.login()
        self.usar_llm(LLMFalso([pergunta("Que disciplinas prefere?"), pergunta("Prefere trabalhar com pessoas?")]))

    def usar_llm(self, llm) -> None:
        self.llm = llm
        self.app.extensions["llm"] = ProtegerDadosPessoais(llm)

    def post(self, caminho: str, client=None, **dados):
        client = client or self.client
        self.set_csrf(client)
        return client.post(caminho, data={"csrf_token": CSRF_TOKEN, **dados})

    def pagina(self) -> str:
        return self.client.get("/orientacao/").get_data(as_text=True)

    def mensagens_guardadas(self) -> list[dict]:
        ligacao = sqlite3.connect(self.db_path)
        try:
            linha = ligacao.execute("SELECT mensagens FROM conversas_orientacao").fetchone()
        finally:
            ligacao.close()
        return json.loads(linha[0]) if linha else []


class AcessoTests(ConversaTestCase):
    def test_sem_sessao_vai_para_o_inicio_de_sessao(self):
        self.logout()
        response = self.client.get("/orientacao/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/auth/entrar", response.headers["Location"])

    def test_abrir_a_pagina_nao_chama_o_llm(self):
        html = self.pagina()
        self.assertIn(texts.ORIENTACAO_COMECAR, html)
        self.assertIn(texts.ORIENTACAO_AVISO, html)
        self.assertEqual(self.llm.pedidos, [])

    def test_os_botoes_exigem_csrf(self):
        for caminho in (
            "/orientacao/comecar", "/orientacao/responder", "/orientacao/tentar-de-novo", "/orientacao/recomecar",
            "/orientacao/sugerir", "/orientacao/continuar",
        ):
            with self.subTest(caminho=caminho):
                self.assertEqual(self.client.post(caminho, data={"resposta": "x"}).status_code, 400)

    def test_a_pagina_inicial_leva_a_conversa(self):
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(texts.HOME_ACTION_CONVERSA, html)
        self.assertIn('href="/orientacao/"', html)


class ConversaConduzidaPeloLLMTests(ConversaTestCase):
    """As perguntas não são fixas: o LLM faz uma de cada vez, a partir das respostas anteriores."""

    def test_comecar_mostra_a_primeira_pergunta_do_llm(self):
        response = self.post("/orientacao/comecar")
        self.assertEqual(response.status_code, 302)
        html = self.pagina()
        self.assertIn("Que disciplinas prefere?", html)
        self.assertIn(texts.ORIENTACAO_RESPOSTA_LABEL, html)
        self.assertEqual(len(self.llm.pedidos), 1)

    def test_comecar_duas_vezes_nao_repete_o_pedido(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/comecar")
        self.assertEqual(len(self.llm.pedidos), 1)

    def test_responder_envia_a_conversa_toda_e_mostra_a_pergunta_seguinte(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        html = self.pagina()
        self.assertIn("Gosto de Informática", html)
        self.assertIn("Prefere trabalhar com pessoas?", html)
        _, enviadas = self.llm.pedidos[1]
        self.assertEqual([m.texto for m in enviadas][1:], ["Que disciplinas prefere?", "Gosto de Informática"])

    def test_o_texto_do_llm_e_mostrado_como_texto_e_nao_como_html(self):
        self.usar_llm(LLMFalso([pergunta("<script>alert(1)</script>")]))
        self.post("/orientacao/comecar")
        html = self.pagina()
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_no_maximo_seis_perguntas(self):
        self.usar_llm(LLMFalso([pergunta("?")] * conversa.LIMITE_PERGUNTAS + [sugestao()]))
        self.post("/orientacao/comecar")
        for i in range(conversa.LIMITE_PERGUNTAS):
            self.post("/orientacao/responder", resposta=f"resposta {i}")
        ultimo, _ = self.llm.pedidos[-1]
        self.assertTrue(ultimo.endswith(conversa.PEDIDO_DE_SUGESTAO))
        html = self.pagina()
        self.assertIn(texts.ORIENTACAO_SUGESTOES_TITULO, html)
        self.assertNotIn(texts.ORIENTACAO_RESPOSTA_LABEL, html)

    def test_resposta_vazia_ou_longa(self):
        self.post("/orientacao/comecar")
        response = self.post("/orientacao/responder", resposta="   ")
        self.assertEqual(response.status_code, 400)
        self.assertIn(texts.ORIENTACAO_ERRO_VAZIA, response.get_data(as_text=True))
        longa = "a" * (conversa.MAX_CARACTERES_RESPOSTA + 1)
        response = self.post("/orientacao/responder", resposta=longa)
        self.assertEqual(response.status_code, 400)
        self.assertIn(longa, response.get_data(as_text=True))   # o texto escrito não se perde
        self.assertEqual(len(self.llm.pedidos), 1)


class DadosPessoaisTests(ConversaTestCase):
    """RNF12: o LLM nunca recebe o email da conta; o que o aluno escreve vai sem emails nem números."""

    def test_o_email_da_conta_nunca_e_enviado(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de dados")
        for instrucoes, mensagens in self.llm.pedidos:
            self.assertNotIn(VALID_EMAIL, instrucoes + " ".join(m.texto for m in mensagens))

    def test_emails_e_telefones_escritos_sao_apagados_antes_de_enviar_e_de_guardar(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Sou a ana@gmail.com, 912 345 678")
        _, enviadas = self.llm.pedidos[1]
        self.assertEqual(enviadas[-1].texto, f"Sou a {EMAIL_REMOVIDO}, {NUMERO_REMOVIDO}")
        self.assertEqual(self.mensagens_guardadas()[-2]["texto"], f"Sou a {EMAIL_REMOVIDO}, {NUMERO_REMOVIDO}")

    def test_a_conversa_fica_no_servidor_e_nao_no_cookie(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        with self.client.session_transaction() as sessao:
            self.assertNotIn("Gosto de Informática", json.dumps(dict(sessao)))
        self.assertEqual(len(self.mensagens_guardadas()), 3)

    def test_cada_aluno_ve_so_a_sua_conversa(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="resposta secreta")
        self.create_active_user(email="outra@gmail.com")
        outro = self.app.test_client()
        self.login(outro, email="outra@gmail.com")
        html = outro.get("/orientacao/").get_data(as_text=True)
        self.assertNotIn("resposta secreta", html)
        self.assertIn(texts.ORIENTACAO_COMECAR, html)


class FalhasDoLLMTests(ConversaTestCase):
    """Se o LLM falhar, aparece uma mensagem clara e a pessoa tenta de novo sem perder a conversa.

    O detalhe técnico fica no registo da aplicação (para a equipa), nunca na página.
    """

    def post_com_falha(self, caminho: str, **dados):
        with self.assertLogs(self.app.logger, level="WARNING"):
            return super().post(caminho, **dados)

    def test_falha_ao_responder_guarda_a_resposta_e_permite_tentar_de_novo(self):
        self.post("/orientacao/comecar")
        self.usar_llm(LLMQueFalha(LLMIndisponivel("sem rede"), 1, [pergunta("Segunda pergunta?")]))
        self.post_com_falha("/orientacao/responder", resposta="Gosto de Gestão")
        html = self.pagina()
        self.assertIn("Gosto de Gestão", html)
        self.assertIn(texts.ORIENTACAO_A_ESPERA, html)
        self.assertIn(texts.ORIENTACAO_TENTAR_DE_NOVO, html)
        self.post("/orientacao/tentar-de-novo")
        html = self.pagina()
        self.assertIn("Segunda pergunta?", html)
        self.assertNotIn(texts.ORIENTACAO_A_ESPERA, html)

    def test_a_mensagem_de_erro_e_clara(self):
        self.usar_llm(LLMQueFalha(LLMIndisponivel("detalhe técnico"), 1, [pergunta("?")]))
        self.post_com_falha("/orientacao/comecar")
        html = self.pagina()
        self.assertIn(texts.ORIENTACAO_ERRO_LLM, html)
        self.assertNotIn("detalhe técnico", html)
        self.assertIn(texts.ORIENTACAO_COMECAR, html)   # pode tentar de novo

    def test_limite_atingido_tem_mensagem_propria(self):
        self.usar_llm(LLMQueFalha(LimiteAtingido("429"), 1, [pergunta("?")]))
        self.post_com_falha("/orientacao/comecar")
        self.assertIn(texts.ORIENTACAO_ERRO_LIMITE, self.pagina())

    def test_resposta_fora_do_formato_tambem_e_tratada(self):
        self.usar_llm(LLMFalso(["isto não é JSON"]))
        self.post_com_falha("/orientacao/comecar")
        self.assertIn(texts.ORIENTACAO_ERRO_LLM, self.pagina())

    def test_fornecedor_sem_chave_nao_rebenta_a_pagina(self):
        del self.app.extensions["llm"]
        self.app.config.update(LLM_BACKEND="gemini", GEMINI_API_KEY="")
        self.post_com_falha("/orientacao/comecar")
        self.assertIn(texts.ORIENTACAO_ERRO_LLM, self.pagina())


class RecomecarTests(ConversaTestCase):
    def test_recomecar_apaga_a_conversa(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        self.post("/orientacao/recomecar")
        self.assertEqual(self.mensagens_guardadas(), [])
        html = self.pagina()
        self.assertNotIn("Gosto de Informática", html)
        self.assertIn(texts.ORIENTACAO_COMECAR, html)


class PercursoTests(ConversaTestCase):
    def test_conversa_terminada_avanca_o_percurso(self):
        self.usar_llm(LLMFalso([sugestao()]))
        self.post("/orientacao/comecar")
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(texts.HOME_ACTION_CONTINUAR, html)
        self.assertNotIn(texts.HOME_ACTION_CONVERSA, html)
