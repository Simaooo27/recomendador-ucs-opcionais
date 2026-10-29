"""US37: o assistente tem em conta as provas que fiz e a minha nota (só com autorização)."""
from __future__ import annotations

import json
import sqlite3
import unittest
from pathlib import Path

from app import texts
from app.candidatura.calculos import Notas, provas_em_falta
from app.catalogo import repository as catalogo_repository
from app.llm.adaptadores import LLMFalso
from app.orientacao import conversa, notas
from tests.test_conversa import ConversaTestCase, pergunta

# O catálogo do MVP (o dos outros testes) não tem condições de acesso: aqui usa-se o recolhido da DGES
# (174 cursos, acima de MAX_CURSOS_DIRETO, por isso a conversa usa o filtro por área).
CATALOGO_COMPLETO = str(Path(__file__).resolve().parent.parent / "dados" / "catalogo-cursos.csv")
CATALOGO = catalogo_repository.todos(CATALOGO_COMPLETO)
NOMES = catalogo_repository.nomes_das_provas(CATALOGO_COMPLETO)
PORTUGUES_E_MAT_A = {"18": 143.0, "19": 157.0}
SO_FRANCES = {"08": 151.0}    # quase nenhum curso pede só Francês: o filtro não se aplica

# Um curso a que falta uma prova com Português e Matemática A, e um a que não falta.
COM_FALTA = next(c for c in CATALOGO if provas_em_falta(c, Notas(15.2, PORTUGUES_E_MAT_A)))
SEM_FALTA = next(c for c in CATALOGO if c.provas and not provas_em_falta(c, Notas(15.2, PORTUGUES_E_MAT_A)))
CONTEXTO = "## O que a pessoa já fez"


def areas(*nomes_das_areas: str) -> str:
    return json.dumps({"tipo": "areas", "areas": list(nomes_das_areas), "localidades": []})


def sugestao(*chaves: str) -> str:
    return json.dumps({"tipo": "sugestao", "texto": "Sugestões.", "cursos": [{"id": c, "explicacao": "Combina."} for c in chaves]})


class FuncoesTests(unittest.TestCase):
    def test_intervalo_da_media_de_2_valores(self):
        casos = {15.2: (14, 16), 14.0: (14, 16), 13.99: (12, 14), 9.5: (10, 12), 19.6: (18, 20), 20.0: (18, 20)}
        for media, esperado in casos.items():
            with self.subTest(media=media):
                self.assertEqual(notas.intervalo_da_media(media), esperado)

    def test_o_contexto_tem_os_exames_e_o_intervalo_mas_nunca_as_notas(self):
        texto = notas.contexto(Notas(15.2, PORTUGUES_E_MAT_A), NOMES)
        self.assertIn(CONTEXTO, texto)
        self.assertIn("Matemática A, Português", texto)
        self.assertIn("entre 14 e 16 valores", texto)
        for exato in ("15.2", "15,2", "143", "157"):
            self.assertNotIn(exato, texto)

    def test_sem_exames_nao_ha_contexto(self):
        self.assertEqual(notas.contexto(Notas(15.2, {}), NOMES), "")
        self.assertFalse(notas.tem_o_que_partilhar(Notas(15.2, {})))

    def test_sem_media_vai_so_a_lista_de_exames(self):
        texto = notas.contexto(Notas(None, {"18": 140.0}), NOMES)
        self.assertIn("Português", texto)
        self.assertNotIn("Média", texto)

    def test_provas_em_falta(self):
        self.assertTrue(provas_em_falta(COM_FALTA, Notas(None, PORTUGUES_E_MAT_A)))
        self.assertEqual(provas_em_falta(SEM_FALTA, Notas(None, PORTUGUES_E_MAT_A)), ())
        sem_regras = next(c for c in CATALOGO if not c.provas)
        self.assertEqual(provas_em_falta(sem_regras, Notas(None, {})), ())

    def test_o_catalogo_enviado_nao_tem_cursos_com_prova_em_falta(self):
        enviados = {c.chave for c in notas.cursos_para_enviar(CATALOGO, Notas(15.2, PORTUGUES_E_MAT_A))}
        self.assertNotIn(COM_FALTA.chave, enviados)
        self.assertIn(SEM_FALTA.chave, enviados)

    def test_com_poucos_cursos_possiveis_vai_o_catalogo_inteiro(self):
        self.assertEqual(len(notas.cursos_para_enviar(CATALOGO, Notas(15.2, SO_FRANCES))), len(CATALOGO))


class AssistenteComNotasTestCase(ConversaTestCase):
    config_overrides = {"CATALOGO_CSV": CATALOGO_COMPLETO}

    def guardar_notas(self, exames: dict, media: float | None = 15.2) -> None:
        ligacao = sqlite3.connect(self.db_path)
        try:
            ligacao.execute(
                "INSERT INTO planos_candidatura (user_id, media, exames, opcoes, atualizado_em) VALUES (?, ?, ?, '[]', '2026-10-29')",
                (self.fetch_user()["id"], media, json.dumps(exames)),
            )
            ligacao.commit()
        finally:
            ligacao.close()

    def usar_notas_guardado(self) -> bool:
        ligacao = sqlite3.connect(self.db_path)
        try:
            return bool(ligacao.execute("SELECT usar_notas FROM conversas_orientacao").fetchone()[0])
        finally:
            ligacao.close()

    def conversa_ate_ao_fim(self, *, usar_notas: bool, resposta_final: str, exames: dict = PORTUGUES_E_MAT_A) -> str:
        """Uma pergunta, uma resposta e a sugestão. Sem filtro (174 cursos) a conversa usa o filtro por
        área (áreas e, a seguir, a sugestão); com o filtro das notas (120 cursos) o catálogo vai inteiro."""
        enviados = notas.cursos_para_enviar(CATALOGO, Notas(15.2, exames)) if usar_notas else CATALOGO
        if len(enviados) > conversa.MAX_CURSOS_DIRETO:
            respostas = [pergunta("Do que gosta?"), areas(COM_FALTA.area, SEM_FALTA.area), resposta_final]
        else:
            respostas = [pergunta("Do que gosta?"), resposta_final]
        self.usar_llm(LLMFalso(respostas))
        dados = {"usar_notas": "on"} if usar_notas else {}
        self.post("/orientacao/comecar", **dados)
        self.post("/orientacao/responder", resposta="Gosto de organizar informação")
        return self.pagina()


class AutorizacaoTests(AssistenteComNotasTestCase):
    """Critério: só com autorização da pessoa."""

    def test_sem_notas_no_plano_nao_ha_caixa_mas_ha_a_ligacao_para_o_plano(self):
        html = self.pagina()
        self.assertNotIn('name="usar_notas"', html)
        self.assertIn('href="/candidatura/notas"', html)

    def test_com_exames_a_caixa_diz_o_que_o_assistente_recebe(self):
        self.guardar_notas(PORTUGUES_E_MAT_A)
        html = self.pagina()
        self.assertIn('name="usar_notas"', html)
        self.assertNotIn('name="usar_notas" type="checkbox" checked', html)   # não vem marcada
        self.assertIn("Matemática A, Português", html)
        self.assertIn("entre 14 e 16 valores", html)
        self.assertNotIn("15,2", html)

    def test_sem_autorizacao_o_llm_nao_recebe_nada_das_notas(self):
        self.guardar_notas(PORTUGUES_E_MAT_A)
        self.conversa_ate_ao_fim(usar_notas=False, resposta_final=sugestao(SEM_FALTA.chave, COM_FALTA.chave))
        self.assertTrue(self.llm.pedidos)
        for instrucoes, _ in self.llm.pedidos:
            self.assertNotIn(CONTEXTO, instrucoes)
        self.assertFalse(self.usar_notas_guardado())

    def test_com_autorizacao_todos_os_pedidos_levam_as_provas_e_o_intervalo(self):
        self.guardar_notas(PORTUGUES_E_MAT_A)
        html = self.conversa_ate_ao_fim(usar_notas=True, resposta_final=sugestao(SEM_FALTA.chave))
        self.assertTrue(self.usar_notas_guardado())
        self.assertEqual(len(self.llm.pedidos), 2)   # a pergunta e a sugestão
        for instrucoes, mensagens in self.llm.pedidos:
            with self.subTest(pedido=instrucoes[-80:]):
                self.assertIn(CONTEXTO, instrucoes)
                self.assertIn("entre 14 e 16 valores", instrucoes)
                tudo = instrucoes + " ".join(m.texto for m in mensagens)
                for exato in ("15.2", "15,2", "143", "157"):
                    self.assertNotIn(exato, tudo.split(CONTEXTO, 1)[1] if CONTEXTO in tudo else tudo)
        self.assertIn(texts.ORIENTACAO_NOTAS_LIGADO, html)

    def test_a_media_exata_nunca_vai_para_o_llm(self):
        """RNF12: nem nas instruções nem nas mensagens."""
        self.guardar_notas({"18": 143.0, "19": 157.0}, media=15.37)
        self.conversa_ate_ao_fim(usar_notas=True, resposta_final=sugestao(SEM_FALTA.chave))
        for instrucoes, mensagens in self.llm.pedidos:
            texto = instrucoes + " ".join(m.texto for m in mensagens)
            self.assertNotIn("15.37", texto)
            self.assertNotIn("15,37", texto)

    def test_pedir_a_autorizacao_sem_exames_no_plano_nao_liga_nada(self):
        self.post("/orientacao/comecar", usar_notas="on")
        self.assertFalse(self.usar_notas_guardado())
        self.assertNotIn(CONTEXTO, self.llm.pedidos[0][0])

    def test_recomecar_tira_a_autorizacao(self):
        self.guardar_notas(PORTUGUES_E_MAT_A)
        self.post("/orientacao/comecar", usar_notas="on")
        self.assertTrue(self.usar_notas_guardado())
        self.post("/orientacao/recomecar")
        self.post("/orientacao/comecar")
        self.assertFalse(self.usar_notas_guardado())


class CursosComProvaEmFaltaTests(AssistenteComNotasTestCase):
    """Critério: cursos a que falta uma prova não são sugeridos, ou vêm assinalados."""

    def test_os_cursos_com_prova_em_falta_nao_vao_para_o_llm(self):
        self.guardar_notas(PORTUGUES_E_MAT_A)
        self.conversa_ate_ao_fim(usar_notas=True, resposta_final=sugestao(SEM_FALTA.chave))
        pedido_final = self.llm.pedidos[-1][0]
        self.assertNotIn(COM_FALTA.chave, pedido_final)

    def test_um_curso_com_prova_em_falta_que_o_llm_invente_e_descartado(self):
        """O LLM não recebeu o curso, por isso a sugestão dele é descartada (RN09)."""
        self.guardar_notas(PORTUGUES_E_MAT_A)
        html = self.conversa_ate_ao_fim(usar_notas=True, resposta_final=sugestao(COM_FALTA.chave, SEM_FALTA.chave))
        self.assertNotIn(f'data-chave="{COM_FALTA.chave}"', html)

    def test_sem_filtro_o_curso_vem_assinalado_com_a_prova_que_falta(self):
        """Com poucos cursos possíveis, vai o catálogo inteiro e a página assinala a prova em falta."""
        self.guardar_notas(SO_FRANCES)
        falta = next(c for c in CATALOGO if c.area and provas_em_falta(c, Notas(15.2, SO_FRANCES)))
        outro = next(c for c in CATALOGO if c.area == falta.area and c.chave != falta.chave)
        self.usar_llm(LLMFalso([pergunta("Do que gosta?"), areas(falta.area), sugestao(falta.chave, outro.chave)]))
        self.post("/orientacao/comecar", usar_notas="on")
        self.post("/orientacao/responder", resposta="Gosto de organizar informação")
        html = self.pagina()
        self.assertIn(f'data-chave="{falta.chave}"', html)
        em_falta = provas_em_falta(falta, Notas(15.2, SO_FRANCES))
        esperado = texts.ORIENTACAO_FALTA_PROVA.format(provas=texts.ORIENTACAO_FALTA_PROVA_JUNTAR.join(NOMES.get(p, p) for p in em_falta))
        self.assertIn(esperado.replace("'", "&#39;"), html)

    def test_sem_autorizacao_nao_se_assinala_nada(self):
        self.guardar_notas(SO_FRANCES)
        falta = next(c for c in CATALOGO if c.area and provas_em_falta(c, Notas(15.2, SO_FRANCES)))
        outro = next(c for c in CATALOGO if c.area == falta.area and c.chave != falta.chave)
        self.usar_llm(LLMFalso([pergunta("Do que gosta?"), areas(falta.area), sugestao(falta.chave, outro.chave)]))
        self.post("/orientacao/comecar")
        self.post("/orientacao/responder", resposta="Gosto de organizar informação")
        self.assertNotIn('class="curso-aviso"', self.pagina())
