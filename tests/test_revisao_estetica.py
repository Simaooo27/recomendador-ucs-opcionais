"""Revisão estética de 23/10 (pedido do PO): barra do topo com lupa e conta, «A minha conta»,
página inicial reorganizada e pesquisa sem resultados pela escola nem por pedaços de palavras."""
from __future__ import annotations

import re

from app import texts
from app.catalogo import services
from app.config import default_config
from tests.base import VALID_EMAIL, AppTestCase


def _acoes(html: str) -> str:
    encontrado = re.search(r'<div class="topo-acoes">.*?</details>\s*</div>', html, re.S)
    return encontrado.group(0) if encontrado else ""


class BarraDoTopoTests(AppTestCase):
    def test_sem_sessao_a_conta_tem_entrar_e_criar_conta(self):
        for pagina in ("/", "/cursos/", "/privacidade"):
            with self.subTest(pagina=pagina):
                acoes = _acoes(self.client.get(pagina).get_data(as_text=True))
                self.assertIn(f'aria-label="{texts.NAV_PROCURAR}"', acoes)
                self.assertIn(f'aria-label="{texts.NAV_CONTA}"', acoes)
                self.assertIn('href="/auth/entrar"', acoes)
                self.assertIn('href="/auth/registo"', acoes)

    def test_a_lupa_procura_na_apresentacao_ou_no_catalogo(self):
        self.assertIn('action="/#resultados"', _acoes(self.client.get("/").get_data(as_text=True)))
        self.assertIn('action="/cursos/"', _acoes(self.client.get("/privacidade").get_data(as_text=True)))

    def test_com_sessao_a_conta_tem_a_minha_conta_e_terminar_sessao(self):
        self.create_active_user()
        self.login()
        acoes = _acoes(self.client.get("/inicio").get_data(as_text=True))
        self.assertIn(VALID_EMAIL, acoes)
        self.assertIn('href="/auth/conta"', acoes)
        self.assertIn('action="/auth/sair"', acoes)
        self.assertNotIn('href="/auth/entrar"', acoes)

    def test_a_barra_fica_encostada_as_margens(self):
        from pathlib import Path

        css = (Path(self.app.static_folder) / "style.css").read_text(encoding="utf-8")
        # Desde o visual calmo (29/10) a apresentação usa a mesma barra que as outras páginas.
        regra = re.search(r"\n\.site-header \{([^}]*)\}", css).group(1)
        self.assertIn("var(--margem)", regra)        # encostada às margens, não centrada como o conteúdo
        self.assertNotIn("padding-inline", regra)


class MinhaContaTests(AppTestCase):
    def test_sem_sessao_vai_para_o_inicio_de_sessao(self):
        response = self.client.get("/auth/conta")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/auth/entrar"))

    def test_mostra_o_email_e_a_ligacao_para_apagar(self):
        self.create_active_user()
        self.login()
        html = self.client.get("/auth/conta").get_data(as_text=True)
        self.assertIn(f"<h1>{texts.CONTA_TITLE}</h1>", html)
        self.assertIn(VALID_EMAIL, html)
        self.assertIn(texts.CONTA_DESDE, html)
        self.assertIn(texts.HOME_CONTA_APAGAR, html)

    def test_cancelar_apagar_volta_a_minha_conta(self):
        self.create_active_user()
        self.login()
        html = self.client.get("/auth/conta/apagar").get_data(as_text=True)
        self.assertIn(f'<a href="/auth/conta">{texts.APAGAR_CANCELAR}</a>', html)


class InicioTests(AppTestCase):
    def test_tem_os_atalhos(self):
        self.create_active_user()
        self.login()
        html = self.client.get("/inicio").get_data(as_text=True)
        for atalho, destino in zip(texts.HOME_ATALHOS, ("/orientacao/", "/cursos/", "/candidatura/"), strict=True):
            with self.subTest(atalho=atalho["titulo"]):
                self.assertIn(atalho["titulo"], html)
                self.assertIn(f'href="{destino}"', html)


class PesquisaTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.config = default_config()

    def _nomes(self, termo):
        return [(c.curso, c.instituicao) for c in services.pesquisar(self.config, termo).cursos]

    def test_a_escola_nao_conta_para_a_pesquisa(self):
        """«gestão» não traz Engenharia Informática só por ser numa «Escola … e Gestão»."""
        for curso in services.pesquisar(self.config, "gestão").cursos:
            with self.subTest(curso=curso.curso):
                texto = " ".join((curso.curso, curso.area)).lower()
                self.assertIn("gest", texto)

    def test_pedacos_do_meio_das_palavras_nao_encontram_nada(self):
        self.assertEqual(services.pesquisar(self.config, "ti").total, 0)
        self.assertGreater(services.pesquisar(self.config, "gest").total, 0)   # o início da palavra encontra

    def test_o_nome_exato_vem_primeiro(self):
        nomes = self._nomes("gestão")
        exatos = [i for i, (curso, _) in enumerate(nomes) if curso == "Gestão"]
        outros = [i for i, (curso, _) in enumerate(nomes) if curso != "Gestão"]
        self.assertTrue(exatos and outros)
        self.assertLess(max(exatos), min(outros))

    def test_os_filtros_do_catalogo_seguem_as_mesmas_regras(self):
        filtros = services.ler_filtros({"q": "ti"}, self.config)
        self.assertEqual(services.filtrar(self.config, filtros), [])


class ComparacaoTests(AppTestCase):
    """A comparação (US05) redesenhada a 23/10: grupos de linhas, duração em anos e saídas em lista."""

    def test_grupos_duracao_e_saidas(self):
        cursos = [c for c in services.cursos(default_config()) if c.saidas][:2]
        pagina = self.client.get("/cursos/comparar?" + "&".join(f"c={c.chave}" for c in cursos)).get_data(as_text=True)
        for grupo in (texts.COMPARAR_GRUPO_NUMEROS, texts.COMPARAR_GRUPO_ONDE, texts.COMPARAR_GRUPO_CURSO):
            self.assertIn(grupo, pagina)
        self.assertIn(texts.COMPARAR_DURACAO.format(anos="3", semestres=6), pagina)
        self.assertIn('<ul class="comparacao-saidas">', pagina)
        self.assertIn(f"<li>{cursos[0].lista_saidas[1]}</li>", pagina)
        self.assertTrue(cursos[0].lista_saidas[1][0].isupper())   # cada saída começa por maiúscula
