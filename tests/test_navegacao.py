"""Menu dos alunos, logótipo com ligação e textos da página inicial (revisão de 22/10)."""
from __future__ import annotations

import re
from pathlib import Path

from app import texts
from app.percurso import EstadoPercurso, passos
from tests.base import VALID_EMAIL, AppTestCase

MENU = {
    "/inicio": texts.NAV_INICIO,
    "/orientacao/": texts.NAV_CONVERSA,
    "/cursos/": texts.NAV_CATALOGO,
    "/percurso/": texts.NAV_DECISOES,
}


def _menu(html: str) -> str:
    encontrado = re.search(r'<nav class="user-nav".*?</nav>', html, re.S)
    return encontrado.group(0) if encontrado else ""


class MenuDosAlunosTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.create_active_user()
        self.login()

    def test_o_menu_tem_as_quatro_paginas(self):
        menu = _menu(self.client.get("/inicio").get_data(as_text=True))
        for caminho, nome in MENU.items():
            with self.subTest(pagina=nome):
                self.assertIn(f'href="{caminho}"', menu)
                self.assertIn(nome, menu)

    def test_a_pagina_atual_fica_marcada(self):
        for caminho, nome in MENU.items():
            with self.subTest(pagina=nome):
                menu = _menu(self.client.get(caminho).get_data(as_text=True))
                marcadas = re.findall(r'<a href="([^"]+)" aria-current="page">', menu)
                self.assertEqual(marcadas, [caminho])

    def test_o_logotipo_leva_ao_inicio(self):
        html = self.client.get("/cursos/").get_data(as_text=True)
        self.assertIn('<a class="marca-ligacao" href="/inicio">', html)

    def test_sem_sessao_nao_ha_menu(self):
        self.logout()
        html = self.client.get("/cursos/").get_data(as_text=True)
        self.assertEqual(_menu(html), "")
        self.assertIn('<a class="marca-ligacao" href="/">', html)

    def test_o_inicio_diz_ola_e_com_que_conta_se_entrou(self):
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(f"<h1>{texts.HOME_GREETING}</h1>", html)
        self.assertNotIn(f"<h1>Olá, {VALID_EMAIL}", html)
        self.assertIn(texts.HOME_SESSAO.format(email=VALID_EMAIL), html)


class MenuDaGestaoTests(AppTestCase):
    def test_o_administrador_nao_ve_o_menu_dos_alunos(self):
        from app.db import get_db
        from app.gestao import services as gestao

        with self.app.app_context():
            gestao.create_admin(get_db(), "admin", "Palavra-passe-1!", "Palavra-passe-1!", self.app.config, created_by=None)
        self.login(email="admin", password="Palavra-passe-1!")
        html = self.client.get("/gestao/").get_data(as_text=True)
        self.assertNotIn(texts.NAV_CONVERSA, html)
        self.assertIn('<a class="marca-ligacao" href="/gestao/">', html)


class PassosConcluidosTests(AppTestCase):
    def test_passo_concluido_deixa_de_ter_o_texto_de_instrucao(self):
        conversa = passos(EstadoPercurso.A_ESCOLHER_CURSO)[1]
        self.assertEqual(conversa.situacao, "feito")
        self.assertEqual(conversa.texto, texts.HOME_PATH_STEPS[1]["feito"])

    def test_passo_por_fazer_mantem_a_instrucao(self):
        conversa = passos(EstadoPercurso.SEM_CURSO)[1]
        self.assertEqual(conversa.texto, texts.HOME_PATH_STEPS[1]["texto"])


class CampoDePesquisaTests(AppTestCase):
    def test_o_campo_de_pesquisa_tem_o_estilo_das_outras_caixas(self):
        css = (Path(self.app.static_folder) / "style.css").read_text(encoding="utf-8")
        # A regra comum das caixas também inclui «select» desde a US05 (filtros do catálogo).
        regra = re.search(r"((?:(?:input\[type=\"\w+\"\]|select),\s*)+)textarea \{", css)
        self.assertIsNotNone(regra)
        self.assertIn('input[type="search"]', regra.group(1))
