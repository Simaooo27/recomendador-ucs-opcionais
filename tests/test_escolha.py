"""US31 — Escolher curso e linha do tempo do percurso, com o LLM falso (sem rede)."""
from __future__ import annotations

import json
import sqlite3
from html import escape

from app import texts
from app.llm.adaptadores import LLMFalso
from tests.base import CSRF_TOKEN
from tests.test_conversa import ConversaTestCase, pergunta
from tests.test_sugestoes import CATALOGO, sugestao

A, B, C = CATALOGO[:3]


class EscolhaTestCase(ConversaTestCase):
    def receber_sugestoes(self, *cursos) -> None:
        """Conversa até o assistente sugerir ``cursos`` (por omissão A e B)."""
        cursos = cursos or (A, B)
        self.usar_llm(LLMFalso([pergunta("Do que gosta?"), sugestao(*[(c.chave, f"Porque {c.curso}.") for c in cursos])]))
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de organizar informação")

    def escolher(self, curso, client=None):
        return self.post(f"/percurso/escolher/{curso.chave}", client=client)

    def decisoes_guardadas(self) -> list[dict]:
        ligacao = sqlite3.connect(self.db_path)
        ligacao.row_factory = sqlite3.Row
        try:
            return [dict(linha) for linha in ligacao.execute("SELECT * FROM decisoes ORDER BY id")]
        finally:
            ligacao.close()

    def linha_tempo(self) -> str:
        return self.client.get("/percurso/").get_data(as_text=True)

    def inicio(self) -> str:
        return self.client.get("/inicio").get_data(as_text=True)


class AcessoTests(EscolhaTestCase):
    def test_sem_sessao_vai_para_o_inicio_de_sessao(self):
        anonimo = self.app.test_client()
        for caminho in ("/percurso/", f"/percurso/escolher/{A.chave}"):
            with self.subTest(caminho=caminho):
                resposta = anonimo.get(caminho)
                self.assertEqual(resposta.status_code, 302)
                self.assertIn("/auth/entrar", resposta.headers["Location"])

    def test_escolher_exige_csrf(self):
        self.assertEqual(self.client.post(f"/percurso/escolher/{A.chave}").status_code, 400)
        self.assertEqual(self.decisoes_guardadas(), [])

    def test_so_cursos_do_catalogo(self):
        self.assertEqual(self.client.get("/percurso/escolher/9999-XXXX").status_code, 404)
        self.set_csrf(self.client)
        resposta = self.client.post("/percurso/escolher/9999-XXXX", data={"csrf_token": CSRF_TOKEN})
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(self.decisoes_guardadas(), [])


class EscolhaConfirmadaTests(EscolhaTestCase):
    """RN10: a escolha nunca é automática; o utilizador confirma."""

    def test_os_cursos_sugeridos_levam_a_confirmacao(self):
        self.receber_sugestoes()
        html = self.pagina()
        for curso in (A, B):
            self.assertIn(f'href="/percurso/escolher/{curso.chave}"', html)
        self.assertEqual(self.decisoes_guardadas(), [])   # receber sugestões não escolhe nada

    def test_abrir_a_confirmacao_nao_regista_nada(self):
        self.receber_sugestoes()
        html = self.client.get(f"/percurso/escolher/{A.chave}").get_data(as_text=True)
        self.assertIn(texts.PERCURSO_CONFIRMAR, html)
        self.assertIn(escape(A.curso), html)
        self.assertIn(texts.PERCURSO_CONVERSA_APAGADA, html)
        self.assertEqual(self.decisoes_guardadas(), [])

    def test_confirmar_regista_a_escolha(self):
        self.receber_sugestoes()
        resposta = self.escolher(A)
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(len(self.decisoes_guardadas()), 1)
        self.assertIn(escape(texts.PERCURSO_ESCOLHA_REGISTADA.format(curso=A.curso, instituicao=A.instituicao)), self.linha_tempo())


class CursoNoPerfilTests(EscolhaTestCase):
    """RF03: depois de escolher, o curso e a instituição ficam no perfil."""

    def test_a_pagina_inicial_mostra_o_curso_e_o_percurso_avanca(self):
        self.receber_sugestoes()
        self.escolher(A)
        html = self.inicio()
        self.assertIn(escape(texts.HOME_CURSO_ESCOLHIDO.format(curso=A.curso, instituicao=A.instituicao)), html)
        self.assertIn(texts.HOME_ACTION_VER_PERCURSO, html)
        self.assertNotIn(texts.HOME_ACTION_CONTINUAR, html)   # já não está «a escolher curso»
        self.assertNotIn(texts.HOME_ACTION_CONVERSA, html)

    def test_cada_aluno_tem_o_seu_curso(self):
        self.receber_sugestoes()
        self.escolher(A)
        outro = self.app.test_client()
        self.create_active_user(email="outra@exemplo.pt")
        self.login(client=outro, email="outra@exemplo.pt")
        html = outro.get("/percurso/").get_data(as_text=True)
        self.assertIn(texts.PERCURSO_VAZIO, html)
        self.assertNotIn(escape(A.curso), html)


class DecisaoRegistadaTests(EscolhaTestCase):
    """RF35: cada decisão fica registada com data, opções sugeridas e opção escolhida."""

    def test_guarda_a_data_os_sugeridos_e_o_escolhido(self):
        self.receber_sugestoes(A, B)
        self.escolher(B)
        decisao = self.decisoes_guardadas()[0]
        self.assertEqual(decisao["curso_chave"], B.chave)
        self.assertEqual(decisao["curso"], B.curso)
        self.assertEqual(decisao["instituicao"], B.instituicao)
        self.assertEqual(decisao["origem"], "sugestao")
        self.assertEqual([s["chave"] for s in json.loads(decisao["sugeridos"])], [A.chave, B.chave])
        self.assertTrue(decisao["decidida_em"].startswith("20"))

    def test_escolher_no_catalogo_sem_conversa(self):
        self.escolher(C)
        decisao = self.decisoes_guardadas()[0]
        self.assertEqual(decisao["origem"], "catalogo")
        self.assertEqual(json.loads(decisao["sugeridos"]), [])

    def test_escolher_outro_do_catalogo_depois_das_sugestoes_guarda_as_sugestoes(self):
        self.receber_sugestoes(A, B)
        self.escolher(C)
        decisao = self.decisoes_guardadas()[0]
        self.assertEqual(decisao["origem"], "catalogo")
        self.assertEqual([s["chave"] for s in json.loads(decisao["sugeridos"])], [A.chave, B.chave])

    def test_a_conversa_e_apagada_depois_de_escolher(self):
        """Ponto 15 dos requisitos (decisão do PO de 20/10): fica só a decisão."""
        self.receber_sugestoes()
        self.escolher(A)
        self.assertEqual(self.mensagens_guardadas(), [])
        self.assertIn(texts.ORIENTACAO_COMECAR, self.pagina())

    def test_a_linha_do_tempo_mostra_a_data_a_origem_e_os_sugeridos(self):
        self.receber_sugestoes(A, B)
        self.escolher(B)
        html = self.linha_tempo()
        self.assertIn(texts.PERCURSO_DA_SUGESTAO, html)
        self.assertIn(texts.PERCURSO_SUGERIDOS, html)
        self.assertIn(escape(A.curso), html)
        self.assertIn('class="decisao-escolhido"', html)
        self.assertIn("<time datetime=", html)


class LinhaDoTempoTests(EscolhaTestCase):
    """Linha do tempo com as decisões, da mais recente para a mais antiga."""

    def test_da_mais_recente_para_a_mais_antiga(self):
        self.escolher(A)
        self.escolher(B)
        self.escolher(C)
        html = self.linha_tempo()
        posicoes = [html.index(f'data-chave="{curso.chave}"') for curso in (C, B, A)]
        self.assertEqual(posicoes, sorted(posicoes))                 # C (a mais recente) aparece primeiro
        self.assertEqual(html.count("decisao-atual"), 1)            # só a mais recente é a atual
        self.assertLess(html.index("decisao-atual"), html.index(f'data-chave="{B.chave}"'))

    def test_sem_decisoes(self):
        html = self.linha_tempo()
        self.assertIn(texts.PERCURSO_VAZIO, html)
        self.assertIn(texts.PERCURSO_NOVA_CONVERSA, html)


class MudarDeCursoTests(EscolhaTestCase):
    """O utilizador pode mudar de curso, o que cria uma nova decisão."""

    def test_mudar_de_curso_cria_uma_nova_decisao(self):
        self.escolher(A)
        self.escolher(B)
        decisoes = self.decisoes_guardadas()
        self.assertEqual([d["curso_chave"] for d in decisoes], [A.chave, B.chave])
        html = self.inicio()
        self.assertIn(escape(texts.HOME_CURSO_ESCOLHIDO.format(curso=B.curso, instituicao=B.instituicao)), html)

    def test_a_confirmacao_avisa_qual_e_o_curso_atual(self):
        self.escolher(A)
        html = self.client.get(f"/percurso/escolher/{B.chave}").get_data(as_text=True)
        self.assertIn(escape(texts.PERCURSO_CURSO_ATUAL.format(curso=A.curso, instituicao=A.instituicao)), html)

    def test_escolher_outra_vez_o_mesmo_curso_nao_cria_decisao(self):
        self.escolher(A)
        self.escolher(A)
        self.assertEqual(len(self.decisoes_guardadas()), 1)
        self.assertIn(texts.PERCURSO_JA_E_O_SEU_CURSO, self.linha_tempo())
        html = self.client.get(f"/percurso/escolher/{A.chave}").get_data(as_text=True)
        self.assertIn(texts.PERCURSO_JA_ESCOLHIDO, html)
        self.assertNotIn(texts.PERCURSO_CONFIRMAR, html)


class CatalogoTests(EscolhaTestCase):
    """«ou outro do catálogo»: a página /cursos/ tem o botão para quem tem sessão iniciada."""

    def test_com_sessao_o_catalogo_tem_o_botao_escolher(self):
        html = self.client.get("/cursos/").get_data(as_text=True)
        self.assertIn(texts.CURSO_ESCOLHER, html)

    def test_sem_sessao_o_catalogo_nao_tem_o_botao(self):
        anonimo = self.app.test_client()
        html = anonimo.get("/cursos/").get_data(as_text=True)
        self.assertNotIn(texts.CURSO_ESCOLHER, html)
        landing = anonimo.get("/").get_data(as_text=True)
        self.assertNotIn(texts.CURSO_ESCOLHER, landing)
