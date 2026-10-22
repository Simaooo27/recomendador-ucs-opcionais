"""US05: consultar e comparar cursos (filtros, ficha completa e comparação de até 3 cursos).

Tudo funciona sem sessão iniciada e sem JavaScript: os filtros e os cursos a comparar vão no endereço.
"""
from __future__ import annotations

import html as html_lib
from urllib.parse import urlencode

from app import texts
from app.catalogo import repository, services
from app.config import default_config
from tests.base import AppTestCase

CATALOGO = repository.todos(default_config()["CATALOGO_CSV"])


def _chaves(pagina: str) -> list[str]:
    """As fichas mostradas na lista, pela ordem (cada uma tem data-chave)."""
    import re

    return re.findall(r'<li class="curso" data-chave="([^"]+)"', pagina)


class FiltrosTests(AppTestCase):
    """Critério 1: filtros por área, instituição e localidade."""

    def _lista(self, **parametros) -> str:
        response = self.client.get("/cursos/?" + urlencode(parametros))
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)

    def test_sem_filtros_mostra_o_catalogo_todo(self):
        pagina = self._lista()
        self.assertEqual(len(_chaves(pagina)), len(CATALOGO))
        self.assertIn(texts.CATALOGO_CONTA_TODOS.format(total=len(CATALOGO)), pagina)

    def test_filtrar_por_area(self):
        chaves = _chaves(self._lista(area="Gestão"))
        esperados = {c.chave for c in CATALOGO if c.area == "Gestão"}
        self.assertEqual(set(chaves), esperados)
        self.assertTrue(esperados)

    def test_filtrar_por_instituicao(self):
        instituicao = CATALOGO[0].instituicao
        chaves = _chaves(self._lista(instituicao=instituicao))
        self.assertEqual(set(chaves), {c.chave for c in CATALOGO if c.instituicao == instituicao})

    def test_filtrar_por_localidade(self):
        chaves = _chaves(self._lista(localidade="Porto"))
        self.assertEqual(set(chaves), {c.chave for c in CATALOGO if c.localidade == "Porto"})

    def test_filtros_combinam_se(self):
        pagina = self._lista(area="Informática", localidade="Lisboa", q="engenharia")
        for chave in _chaves(pagina):
            curso = next(c for c in CATALOGO if c.chave == chave)
            self.assertEqual((curso.area, curso.localidade), ("Informática", "Lisboa"))
        esperados = [c for c in CATALOGO if c.area == "Informática" and c.localidade == "Lisboa"]
        self.assertIn(texts.CATALOGO_CONTA.format(mostrados=len(_chaves(pagina)), total=len(CATALOGO)), pagina)
        self.assertLessEqual(len(_chaves(pagina)), len(esperados))

    def test_o_filtro_escolhido_fica_selecionado(self):
        pagina = self._lista(area="Gestão")
        self.assertIn('<option value="Gestão" selected>', pagina)
        self.assertIn(texts.CATALOGO_LIMPAR, pagina)

    def test_valor_que_nao_existe_e_ignorado(self):
        pagina = self._lista(area="Medicina", instituicao="<script>")
        self.assertEqual(len(_chaves(pagina)), len(CATALOGO))
        self.assertNotIn("<script>", pagina)

    def test_sem_resultados_diz_o_que_fazer(self):
        pagina = self._lista(q="zzzzzz")
        self.assertEqual(_chaves(pagina), [])
        self.assertIn(texts.CATALOGO_VAZIO, pagina)

    def test_as_opcoes_vem_do_catalogo(self):
        opcoes = services.opcoes(default_config())
        self.assertEqual(set(opcoes.areas), {c.area for c in CATALOGO})
        self.assertEqual(len(opcoes.instituicoes), len({c.instituicao for c in CATALOGO}))
        self.assertIn("Évora", opcoes.localidades)
        # Ordem alfabética sem contar acentos: «Évora» fica entre «Coimbra» e «Felgueiras».
        self.assertLess(opcoes.localidades.index("Coimbra"), opcoes.localidades.index("Évora"))
        self.assertLess(opcoes.localidades.index("Évora"), opcoes.localidades.index("Felgueiras"))


class FichaTests(AppTestCase):
    """Critério 2: ficha de cada curso com descrição, saídas, vagas, nota do último colocado e fonte."""

    def setUp(self) -> None:
        super().setUp()
        self.curso = next(c for c in CATALOGO if c.vagas and c.ultimo_colocado and c.saidas)

    def test_ficha_mostra_os_dados_do_curso(self):
        response = self.client.get(f"/cursos/{self.curso.chave}")
        self.assertEqual(response.status_code, 200)
        pagina = html_lib.unescape(response.get_data(as_text=True))
        for valor in (self.curso.curso, self.curso.instituicao, self.curso.descricao, str(self.curso.vagas),
                      self.curso.ultimo_colocado, self.curso.fonte, self.curso.lista_saidas[0]):
            self.assertIn(valor, pagina)
        self.assertIn(texts.FICHA_SAIDAS, pagina)

    def test_curso_que_nao_existe_da_404(self):
        self.assertEqual(self.client.get("/cursos/0000-XXXX").status_code, 404)

    def test_as_fichas_da_lista_levam_a_ficha_completa(self):
        pagina = self.client.get("/cursos/").get_data(as_text=True)
        self.assertIn(f'href="/cursos/{self.curso.chave}"', pagina)

    def test_escolher_so_aparece_com_sessao(self):
        pagina = self.client.get(f"/cursos/{self.curso.chave}").get_data(as_text=True)
        self.assertNotIn(texts.CURSO_ESCOLHER, pagina)
        self.create_active_user()
        self.login()
        pagina = self.client.get(f"/cursos/{self.curso.chave}").get_data(as_text=True)
        self.assertIn(f"/percurso/escolher/{self.curso.chave}", pagina)


class CompararTests(AppTestCase):
    """Critério 3: comparação de até 3 cursos lado a lado."""

    def _comparar(self, *chaves):
        return self.client.get("/cursos/comparar?" + urlencode([("c", c) for c in chaves]))

    def test_a_lista_tem_uma_caixa_comparar_em_cada_ficha(self):
        pagina = self.client.get("/cursos/").get_data(as_text=True)
        self.assertEqual(pagina.count('form="comparar-form"'), len(CATALOGO))
        self.assertIn('id="comparar-form"', pagina)
        self.assertIn('action="/cursos/comparar"', pagina)

    def test_compara_tres_cursos_lado_a_lado(self):
        a, b, c = CATALOGO[:3]
        response = self._comparar(a.chave, b.chave, c.chave)
        self.assertEqual(response.status_code, 200)
        pagina = html_lib.unescape(response.get_data(as_text=True))
        self.assertEqual(pagina.count('<th scope="col">'), 3)
        # A ordem das colunas é a ordem pedida.
        self.assertLess(pagina.index(f'href="/cursos/{a.chave}"'), pagina.index(f'href="/cursos/{b.chave}"'))
        for linha in (texts.LANDING_CARD_VAGAS, texts.LANDING_CARD_NOTA, texts.FICHA_SAIDAS, texts.FICHA_LOCALIDADE):
            self.assertIn(f'<th scope="row">{linha}</th>', pagina)

    def test_compara_dois_cursos(self):
        response = self._comparar(CATALOGO[0].chave, CATALOGO[1].chave)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).count('<th scope="col">'), 2)

    def test_mais_de_tres_ficam_os_tres_primeiros(self):
        response = self._comparar(*(c.chave for c in CATALOGO[:5]))
        pagina = response.get_data(as_text=True)
        self.assertEqual(pagina.count('<th scope="col">'), 3)
        self.assertIn(texts.COMPARAR_A_MAIS.format(maximo=3), pagina)

    def test_menos_de_dois_explica_e_nao_compara(self):
        for chaves in ((), (CATALOGO[0].chave,)):
            with self.subTest(chaves=chaves):
                response = self._comparar(*chaves)
                self.assertEqual(response.status_code, 400)
                pagina = response.get_data(as_text=True)
                self.assertIn(texts.COMPARAR_POUCOS.format(minimo=2), pagina)
                self.assertNotIn('<table class="comparacao">', pagina)

    def test_repetidos_e_inexistentes_ficam_de_fora(self):
        a, b = CATALOGO[:2]
        response = self._comparar(a.chave, a.chave, "0000-XXXX", b.chave)
        pagina = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pagina.count('<th scope="col">'), 2)
        self.assertIn(texts.COMPARAR_IGNORADOS, pagina)


class SemSessaoTests(AppTestCase):
    """Critério 4: funciona sem sessão iniciada."""

    def test_todas_as_paginas_abrem_sem_sessao(self):
        a, b = CATALOGO[:2]
        for endereco in ("/cursos/", "/cursos/?area=Gestão", f"/cursos/{a.chave}", f"/cursos/comparar?c={a.chave}&c={b.chave}"):
            with self.subTest(endereco=endereco):
                response = self.client.get(endereco)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn("/auth/entrar", response.headers.get("Location", ""))
