"""US30 — Sugestão de 2 a 3 cursos no fim da conversa, com o LLM falso (sem rede)."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app import texts
from app.catalogo import repository as catalogo_repository
from app.config import default_config
from app.llm import LLMIndisponivel
from app.llm.adaptadores import LLMFalso
from app.orientacao import conversa
from tests.test_conversa import ConversaTestCase, LLMQueFalha, pergunta

CATALOGO = catalogo_repository.todos(default_config()["CATALOGO_CSV"])
A, B, C, D = CATALOGO[:4]


def sugestao(*itens: tuple[str, str], texto: str = "Estes cursos combinam consigo.") -> str:
    """Resposta do LLM com os cursos (identificador, explicação) dados."""
    return json.dumps({"tipo": "sugestao", "texto": texto, "cursos": [{"id": i, "explicacao": e} for i, e in itens]})


class SugestoesTestCase(ConversaTestCase):
    def conversar_ate_a_sugestao(self, resposta_final: str) -> str:
        """Começa a conversa, responde uma vez e o LLM responde com ``resposta_final``."""
        self.usar_llm(LLMFalso([pergunta("Do que gosta?"), resposta_final]))
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de organizar informação")
        return self.pagina()

    def sugestao_guardada(self) -> dict | None:
        ligacao = sqlite3.connect(self.db_path)
        try:
            linha = ligacao.execute("SELECT sugestao FROM conversas_orientacao").fetchone()
        finally:
            ligacao.close()
        return json.loads(linha[0]) if linha and linha[0] else None


class MostrarSugestoesTests(SugestoesTestCase):
    """Cada curso mostra os dados do catálogo e a explicação do LLM (RF37)."""

    def test_mostra_os_cursos_com_os_dados_do_catalogo_e_a_explicacao(self):
        html = self.conversar_ate_a_sugestao(sugestao((A.chave, "Gosta de organizar informação."), (B.chave, "É perto de casa.")))
        self.assertIn(texts.ORIENTACAO_SUGESTOES_TITULO, html)
        for curso in (A, B):
            with self.subTest(curso=curso.chave):
                self.assertIn(f'data-chave="{curso.chave}"', html)
                self.assertIn(curso.instituicao.replace("'", "&#39;"), html)
                self.assertIn(curso.localidade, html)
                self.assertIn(curso.fonte.replace("&", "&amp;"), html)   # ligação à DGES
                if curso.vagas is not None:
                    self.assertIn(f'data-campo="vagas">{curso.vagas}<', html)
                if curso.ultimo_colocado:
                    self.assertIn(curso.ultimo_colocado, html)
        self.assertIn("Gosta de organizar informação.", html)
        self.assertIn("É perto de casa.", html)
        self.assertIn(texts.ORIENTACAO_PORQUE, html)

    def test_no_maximo_tres_cursos(self):
        html = self.conversar_ate_a_sugestao(sugestao(*((c.chave, "x") for c in (A, B, C, D))))
        self.assertEqual(html.count('class="curso"'), conversa.MAX_CURSOS_SUGERIDOS)
        self.assertNotIn(f'data-chave="{D.chave}"', html)

    def test_a_explicacao_do_llm_e_mostrada_como_texto(self):
        html = self.conversar_ate_a_sugestao(sugestao((A.chave, "<b>negrito</b>"), (B.chave, "x")))
        self.assertNotIn("<b>negrito</b>", html)
        self.assertIn("&lt;b&gt;negrito&lt;/b&gt;", html)

    def test_a_conversa_termina_sem_caixa_de_resposta(self):
        html = self.conversar_ate_a_sugestao(sugestao((A.chave, "x"), (B.chave, "y")))
        self.assertNotIn(texts.ORIENTACAO_RESPOSTA_LABEL, html)
        self.assertNotIn(texts.ORIENTACAO_VER_SUGESTOES, html)


class SoCursosDoCatalogoTests(SugestoesTestCase):
    """RN09: os cursos inventados pelo LLM são descartados antes de chegar ao ecrã."""

    def test_cursos_inventados_nao_aparecem(self):
        resposta = sugestao((A.chave, "x"), ("9999-0000", "Medicina em Harvard"), (B.chave, "y"))
        html = self.conversar_ate_a_sugestao(resposta)
        self.assertNotIn("Medicina em Harvard", html)
        self.assertNotIn("9999-0000", html)
        self.assertEqual(html.count('class="curso"'), 2)
        self.assertEqual(self.sugestao_guardada()["descartados"], ["9999-0000"])

    def test_curso_que_saiu_do_catalogo_depois_de_sugerido_deixa_de_aparecer(self):
        self.conversar_ate_a_sugestao(sugestao((A.chave, "x"), (B.chave, "y")))
        caminho = Path(self.db_path).with_name("catalogo.csv")
        with open(default_config()["CATALOGO_CSV"], encoding="utf-8-sig") as original:
            linhas = original.read().splitlines()
        # Tira o curso A do catálogo (a linha com o código da instituição e o do curso).
        sem_a = [l for l in linhas if f",{A.codigo_instituicao},{A.codigo_curso}," not in l]
        caminho.write_text("\n".join(sem_a) + "\n", encoding="utf-8")
        self.app.config["CATALOGO_CSV"] = str(caminho)
        html = self.pagina()
        self.assertNotIn(f'data-chave="{A.chave}"', html)
        self.assertIn(texts.ORIENTACAO_POUCAS_SUGESTOES, html)


class PoucasSugestoesTests(SugestoesTestCase):
    """Se sobrarem menos de 2 cursos, a página diz isso e propõe continuar ou ver o catálogo."""

    def test_menos_de_dois_cursos_mostra_o_aviso_e_as_duas_saidas(self):
        html = self.conversar_ate_a_sugestao(sugestao((A.chave, "x"), ("inventado", "y")))
        self.assertIn(texts.ORIENTACAO_POUCAS_SUGESTOES, html)
        self.assertIn(texts.ORIENTACAO_CONTINUAR_CONVERSA, html)
        self.assertIn('href="/cursos/"', html)
        self.assertIn(f'data-chave="{A.chave}"', html)   # o que sobrou continua a aparecer
        self.assertNotIn(texts.ORIENTACAO_ESCOLHA_DEPOIS, html)

    def test_nenhum_curso_valido(self):
        html = self.conversar_ate_a_sugestao(sugestao(("inventado", "x")))
        self.assertIn(texts.ORIENTACAO_POUCAS_SUGESTOES, html)
        self.assertNotIn('class="curso"', html)

    def test_continuar_a_conversa_mantem_as_mensagens_e_nao_chama_o_llm(self):
        self.conversar_ate_a_sugestao(sugestao((A.chave, "x")))
        pedidos = len(self.llm.pedidos)
        self.post("/orientacao/continuar")
        self.assertEqual(len(self.llm.pedidos), pedidos)
        self.assertIsNone(self.sugestao_guardada())
        html = self.pagina()
        self.assertIn("Gosto de organizar informação", html)
        self.assertIn(texts.ORIENTACAO_RESPOSTA_LABEL, html)

    def test_depois_de_continuar_a_resposta_seguinte_volta_a_pedir_cursos(self):
        self.usar_llm(LLMFalso(
            [pergunta("?")] * conversa.LIMITE_PERGUNTAS + [sugestao((A.chave, "x")), sugestao((A.chave, "x"), (B.chave, "y"))]
        ))
        self.post("/orientacao/comecar")
        for i in range(conversa.LIMITE_PERGUNTAS):
            self.post("/orientacao/responder", resposta=f"resposta {i}")
        self.assertIn(texts.ORIENTACAO_POUCAS_SUGESTOES, self.pagina())
        self.post("/orientacao/continuar")
        self.assertNotIn(texts.ORIENTACAO_PROGRESSO.split("{")[0], self.pagina())   # já passou das 6 perguntas
        self.post("/orientacao/responder", resposta="Também gosto de gestão")
        instrucoes, _ = self.llm.pedidos[-1]
        self.assertTrue(instrucoes.endswith(conversa.PEDIDO_DE_SUGESTAO))
        self.assertIn(texts.ORIENTACAO_ESCOLHA_DEPOIS, self.pagina())

    def test_com_sugestoes_suficientes_continuar_nao_faz_nada(self):
        self.conversar_ate_a_sugestao(sugestao((A.chave, "x"), (B.chave, "y")))
        self.post("/orientacao/continuar")
        self.assertIsNotNone(self.sugestao_guardada())

    def test_o_catalogo_abre_com_sessao_iniciada(self):
        response = self.client.get("/cursos/?q=" + A.curso)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn(texts.CATALOGO_TITLE, html)
        self.assertIn(f'data-chave="{A.chave}"', html)
        self.assertIn(texts.CATALOGO_VOLTAR, html)

    def test_o_catalogo_sem_resultados(self):
        html = self.client.get("/cursos/?q=zzzzzz").get_data(as_text=True)
        self.assertIn(texts.CATALOGO_VAZIO, html)   # US05: a lista do catálogo tem filtros e mensagem própria


class VerSugestoesJaTests(SugestoesTestCase):
    """A pessoa pode pedir a sugestão antes das 6 respostas («Ver sugestões já»)."""

    def test_o_botao_so_aparece_depois_da_primeira_resposta(self):
        self.post("/orientacao/comecar")
        self.assertNotIn(texts.ORIENTACAO_VER_SUGESTOES, self.pagina())
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        self.assertIn(texts.ORIENTACAO_VER_SUGESTOES, self.pagina())

    def test_pedir_obriga_o_llm_a_sugerir(self):
        self.usar_llm(LLMFalso([pergunta("Do que gosta?"), pergunta("E mais?"), sugestao((A.chave, "x"), (B.chave, "y"))]))
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        response = self.post("/orientacao/sugerir")
        self.assertIn("#sugestoes", response.headers["Location"])
        instrucoes, enviadas = self.llm.pedidos[-1]
        self.assertTrue(instrucoes.endswith(conversa.PEDIDO_DE_SUGESTAO))
        self.assertEqual(enviadas[-1].texto, texts.ORIENTACAO_PEDIDO_SUGESTAO)
        html = self.pagina()
        self.assertIn(texts.ORIENTACAO_PEDIDO_SUGESTAO, html)   # o pedido fica na conversa
        self.assertIn(f'data-chave="{A.chave}"', html)

    def test_antes_de_responder_o_pedido_e_ignorado(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/sugerir")
        self.assertEqual(len(self.llm.pedidos), 1)

    def test_se_o_llm_falhar_tentar_de_novo_volta_a_pedir_as_sugestoes(self):
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        self.usar_llm(LLMQueFalha(LLMIndisponivel("sem rede"), 1, [sugestao((A.chave, "x"), (B.chave, "y"))]))
        with self.assertLogs(self.app.logger, level="WARNING"):
            self.post("/orientacao/sugerir")
        self.assertIn(texts.ORIENTACAO_A_ESPERA, self.pagina())
        self.post("/orientacao/tentar-de-novo")
        instrucoes, _ = self.llm.falso.pedidos[-1]
        self.assertTrue(instrucoes.endswith(conversa.PEDIDO_DE_SUGESTAO))
        self.assertIn(texts.ORIENTACAO_SUGESTOES_TITULO, self.pagina())


    def test_se_o_llm_fizer_outra_pergunta_nao_aparece_e_tentar_de_novo_volta_a_pedir(self):
        """Corrigido a 20/10: pedir as sugestões não pode acabar numa pergunta a mais."""
        self.usar_llm(LLMFalso([pergunta("Do que gosta?"), pergunta("E que disciplinas prefere?")]))
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de Informática")
        self.usar_llm(LLMFalso([pergunta("Desobedeci?"), sugestao((A.chave, "x"), (B.chave, "y"))]))
        with self.assertLogs(self.app.logger, level="WARNING"):
            self.post("/orientacao/sugerir")
        html = self.pagina()
        self.assertNotIn("Desobedeci?", html)
        self.assertIn(texts.ORIENTACAO_A_ESPERA, html)
        self.post("/orientacao/tentar-de-novo")
        instrucoes, _ = self.llm.pedidos[-1]
        self.assertTrue(instrucoes.endswith(conversa.PEDIDO_DE_SUGESTAO))
        self.assertIn(texts.ORIENTACAO_SUGESTOES_TITULO, self.pagina())


class NenhumCursoEscolhidoTests(SugestoesTestCase):
    """RN10: as sugestões nunca atribuem um curso; a escolha é a US31."""

    def test_a_pagina_diz_que_nada_foi_escolhido_e_nao_ha_botao_de_escolher(self):
        html = self.conversar_ate_a_sugestao(sugestao((A.chave, "x"), (B.chave, "y")))
        self.assertIn(texts.ORIENTACAO_ESCOLHA_DEPOIS, html)
        self.assertNotIn("escolher", html.split("sugestoes-titulo")[1].split("</section>")[0].replace(
            texts.ORIENTACAO_ESCOLHA_DEPOIS, ""
        ).lower())

    def test_o_percurso_so_avanca_com_pelo_menos_dois_cursos(self):
        self.conversar_ate_a_sugestao(sugestao((A.chave, "x")))
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(texts.HOME_ACTION_CONVERSA, html)
        self.post("/orientacao/recomecar")
        self.conversar_ate_a_sugestao(sugestao((A.chave, "x"), (B.chave, "y")))
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(texts.HOME_ACTION_CONTINUAR, html)
