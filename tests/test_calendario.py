"""US38: datas do Concurso Nacional de Acesso no plano de candidatura e no percurso."""
from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date
from unittest import mock

from app import texts
from app.candidatura import calendario
from app.candidatura.calendario import PAGINA_DGES, frase_do_prazo, proximo_prazo
from app.config import default_config
from tests.base import AppTestCase

CALENDARIO = calendario.ler(default_config()["CALENDARIO_CSV"])


def _dia_fixo(dia: date):
    """Substitui ``date`` num módulo por uma versão em que «hoje» é ``dia`` (os testes não dependem do relógio)."""

    class _Data(date):
        @classmethod
        def today(cls):
            return dia

    return _Data


class FicheiroTests(unittest.TestCase):
    """Critério: datas das 3 fases do concurso (Despacho n.º 6934/2026)."""

    def test_tem_as_3_fases_de_2026_cada_uma_com_as_3_etapas(self):
        self.assertEqual(CALENDARIO.ano, 2026)
        self.assertEqual([f.numero for f in CALENDARIO.fases], [1, 2, 3])
        for fase in CALENDARIO.fases:
            with self.subTest(fase=fase.numero):
                self.assertEqual([e.etapa for e in fase.etapas], ["candidatura", "resultados", "matricula"])

    def test_datas_do_despacho(self):
        primeira = CALENDARIO.fases[0].etapas
        self.assertEqual((primeira[0].inicio, primeira[0].fim), (date(2026, 7, 20), date(2026, 8, 6)))
        self.assertEqual(primeira[1].inicio, date(2026, 8, 23))
        terceira = CALENDARIO.fases[2].etapas
        self.assertEqual((terceira[2].inicio, terceira[2].fim), (date(2026, 9, 30), date(2026, 10, 2)))

    def test_mostra_o_ano_mais_recente_do_ficheiro(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "calendario.csv")
            with open(caminho, "w", encoding="utf-8") as ficheiro:
                ficheiro.write("ano,fase,etapa,inicio,fim,nota\n")
                ficheiro.write("2026,1,candidatura,2026-07-20,2026-08-06,\n")
                ficheiro.write("2027,1,candidatura,2027-07-19,2027-08-05,\n")
            self.assertEqual(calendario.ler(caminho).ano, 2027)

    def test_sem_ficheiro_o_calendario_fica_vazio(self):
        vazio = calendario.ler("/nao/existe.csv")
        self.assertIsNone(vazio.ano)
        self.assertEqual(vazio.fases, ())

    def test_erros_no_ficheiro_sao_assinalados(self):
        for linha in ("2026,1,exames,2026-07-20,2026-08-06,", "2026,1,candidatura,2026-08-06,2026-07-20,"):
            with self.subTest(linha=linha), tempfile.TemporaryDirectory() as pasta:
                caminho = os.path.join(pasta, "calendario.csv")
                with open(caminho, "w", encoding="utf-8") as ficheiro:
                    ficheiro.write("ano,fase,etapa,inicio,fim,nota\n" + linha + "\n")
                with self.assertRaises(ValueError):
                    calendario.ler(caminho)


class ProximoPrazoTests(unittest.TestCase):
    """Critério: o passo atual do percurso mostra o próximo prazo."""

    def test_antes_do_concurso_e_a_candidatura_a_1a_fase(self):
        prazo = proximo_prazo(CALENDARIO, date(2026, 5, 1))
        self.assertEqual((prazo.etapa.fase, prazo.etapa.etapa, prazo.a_decorrer), (1, "candidatura", False))
        self.assertEqual(frase_do_prazo(prazo), "Candidatura da 1.ª fase: de 20/07/2026 a 06/08/2026.")

    def test_durante_a_candidatura_diz_ate_quando(self):
        prazo = proximo_prazo(CALENDARIO, date(2026, 7, 25))
        self.assertTrue(prazo.a_decorrer)
        self.assertEqual(frase_do_prazo(prazo), "Candidatura da 1.ª fase: até 06/08/2026.")

    def test_no_ultimo_dia_ainda_esta_a_decorrer(self):
        self.assertTrue(proximo_prazo(CALENDARIO, date(2026, 8, 6)).a_decorrer)

    def test_entre_etapas_e_a_seguinte(self):
        prazo = proximo_prazo(CALENDARIO, date(2026, 8, 10))
        self.assertEqual((prazo.etapa.fase, prazo.etapa.etapa), (1, "resultados"))
        self.assertEqual(frase_do_prazo(prazo), "Resultados da 1.ª fase: 23/08/2026.")

    def test_no_dia_dos_resultados(self):
        self.assertEqual(frase_do_prazo(proximo_prazo(CALENDARIO, date(2026, 8, 23))), "Resultados da 1.ª fase: hoje, 23/08/2026.")

    def test_com_duas_etapas_ao_mesmo_tempo_conta_a_que_acaba_primeiro(self):
        # 25/08: matrícula da 1.ª fase (até 27/08) e candidatura à 2.ª (até 02/09).
        prazo = proximo_prazo(CALENDARIO, date(2026, 8, 25))
        self.assertEqual((prazo.etapa.fase, prazo.etapa.etapa), (1, "matricula"))

    def test_depois_do_concurso_diz_que_as_datas_seguintes_ainda_nao_sairam(self):
        prazo = proximo_prazo(CALENDARIO, date(2026, 10, 29))
        self.assertIsNone(prazo.etapa)
        self.assertEqual(prazo.ano_seguinte, 2027)
        self.assertEqual(frase_do_prazo(prazo), texts.HOME_PRAZO_SEM_DATAS.format(ano=2027))

    def test_sem_datas_nenhumas(self):
        prazo = proximo_prazo(calendario.Calendario(None, ()), date(2026, 10, 29))
        self.assertIsNone(prazo.etapa)
        self.assertEqual(prazo.ano_seguinte, 2026)


class PaginasTests(AppTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()
        self.login()

    def _inicio(self, dia: date) -> str:
        with mock.patch("app.main.date", _dia_fixo(dia)):
            return self.client.get("/inicio").get_data(as_text=True)

    def test_o_passo_atual_mostra_o_proximo_prazo(self):
        html = self._inicio(date(2026, 7, 25))
        self.assertIn(texts.HOME_PRAZO_TITULO, html)
        self.assertIn("Candidatura da 1.ª fase: até 06/08/2026.", html)
        self.assertIn(f'href="{PAGINA_DGES}"', html)
        # Só no passo atual: aparece uma vez.
        self.assertEqual(html.count(texts.HOME_PRAZO_TITULO), 1)

    def test_depois_do_concurso_o_percurso_avisa_que_as_datas_ainda_nao_sairam(self):
        self.assertIn(texts.HOME_PRAZO_SEM_DATAS.format(ano=2027), self._inicio(date(2026, 10, 29)))

    def test_o_plano_mostra_as_3_fases_e_a_ligacao_para_a_dges(self):
        with mock.patch("app.candidatura.routes.date", _dia_fixo(date(2026, 7, 25))):
            html = self.client.get("/candidatura/").get_data(as_text=True)
        self.assertIn(texts.CALENDARIO_TITULO, html)
        for fase in (1, 2, 3):
            self.assertIn(texts.CALENDARIO_FASE.format(fase=fase), html)
        for nome in (texts.CALENDARIO_ETAPA_CANDIDATURA, texts.CALENDARIO_ETAPA_RESULTADOS, texts.CALENDARIO_ETAPA_MATRICULA):
            self.assertIn(nome, html)
        self.assertIn("20/07 a 06/08/2026", html)
        self.assertIn(texts.CALENDARIO_A_DECORRER, html)
        self.assertIn(f'href="{PAGINA_DGES}"', html)
        self.assertIn(texts.CALENDARIO_LIGACAO, html)

    def test_o_plano_depois_do_concurso_avisa_e_continua_a_mostrar_as_datas(self):
        with mock.patch("app.candidatura.routes.date", _dia_fixo(date(2026, 10, 29))):
            html = self.client.get("/candidatura/").get_data(as_text=True)
        self.assertIn(texts.CALENDARIO_JA_PASSOU.format(ano=2026, seguinte=2027), html)
        self.assertIn("30/09/2026", html)
        self.assertNotIn(texts.CALENDARIO_A_DECORRER, html)

    def test_sem_ficheiro_o_plano_manda_para_a_dges(self):
        self.app.config["CALENDARIO_CSV"] = "/nao/existe.csv"
        html = self.client.get("/candidatura/").get_data(as_text=True)
        self.assertIn(texts.CALENDARIO_SEM_DATAS, html)
        self.assertIn(f'href="{PAGINA_DGES}"', html)
