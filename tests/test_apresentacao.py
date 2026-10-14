"""Página de apresentação, «O seu percurso», painel com números e detalhes de interação."""
from unittest import mock

from app import manuscrito, percurso, texts
from app.percurso import EstadoPercurso
from tests.base import CSRF_TOKEN, AppTestCase


def _location(response) -> str:
    return response.headers.get("Location", "")


class LandingPageTests(AppTestCase):
    def test_sem_sessao_mostra_a_apresentacao(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn(texts.LANDING_HOW_TITLE, html)
        for opcao in texts.LANDING_PATH_OPTIONS:
            self.assertIn(opcao["nome"], html)
        for passo in texts.LANDING_STEPS:
            self.assertIn(passo["titulo"], html)

    def test_tem_ligacoes_para_criar_conta_e_iniciar_sessao(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('href="/auth/registo"', html)
        self.assertIn('href="/auth/entrar"', html)

    def test_nao_tem_ligacoes_para_a_gestao(self):
        self.assertNotIn("/gestao", self.client.get("/").get_data(as_text=True))

    def test_aluno_com_sessao_vai_para_o_inicio(self):
        self.create_active_user()
        self.login()
        self.assertTrue(_location(self.client.get("/")).endswith("/inicio"))

    def test_administrador_com_sessao_vai_para_a_gestao(self):
        runner = self.app.test_cli_runner()
        runner.invoke(args=["create-admin", "--username", "gestor", "--password", "gestao-segura-1"])
        self.set_csrf()
        self.client.post("/auth/entrar", data={"csrf_token": CSRF_TOKEN, "email": "gestor", "password": "gestao-segura-1"})
        self.assertTrue(_location(self.client.get("/")).endswith("/gestao/"))

    def test_os_controlos_do_mapa_so_aparecem_com_javascript(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("data-mapa-controlos hidden", html)
        self.assertIn(texts.LANDING_PATH_OPTIONS[0]["porque"], html)  # explicação visível sem JavaScript


class HandwritingTests(AppTestCase):
    """O nome do caminho é escrito à mão; sem fontTools aparece texto normal."""

    def test_desenha_um_caminho_por_contorno(self):
        desenho = manuscrito.desenhar("Gestão")
        self.assertIsNotNone(desenho)
        self.assertGreater(len(desenho.contornos), 3)
        self.assertTrue(all(c.startswith("M") for c in desenho.contornos))
        self.assertEqual(len(desenho.viewbox.split()), 4)

    def test_texto_vazio_nao_desenha(self):
        self.assertIsNone(manuscrito.desenhar("   "))

    def test_apresentacao_tem_a_palavra_escrita_com_nome_acessivel(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('class="manuscrito"', html)
        self.assertIn(f'aria-label="{texts.LANDING_PATH_OPTIONS[0]["nome"]}"', html)

    def test_sem_fonttools_mostra_texto_normal(self):
        with mock.patch.object(manuscrito, "desenhar", return_value=None):
            response = self.client.get("/")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="manuscrito-texto"', html)


class PathTimelineTests(AppTestCase):
    """«O seu percurso» na página inicial do aluno (padrão State, app/percurso.py)."""

    def test_sem_curso_o_proximo_passo_e_o_questionario(self):
        passos = percurso.passos(EstadoPercurso.SEM_CURSO)
        self.assertEqual([p.situacao for p in passos], ["feito", "atual", "depois", "depois"])
        self.assertEqual(passos[1].titulo, texts.HOME_PATH_STEPS[1]["titulo"])

    def test_cada_estado_avanca_o_passo_atual(self):
        atuais = [
            [p.situacao for p in percurso.passos(estado)].index("atual")
            for estado in (EstadoPercurso.SEM_CURSO, EstadoPercurso.A_ESCOLHER_CURSO, EstadoPercurso.COM_CURSO)
        ]
        self.assertEqual(atuais, [1, 2, 3])

    def test_pagina_inicial_mostra_a_linha_do_tempo(self):
        self.create_active_user()
        self.login()
        html = self.client.get("/inicio").get_data(as_text=True)
        self.assertIn(texts.HOME_PATH_TITLE, html)
        self.assertIn('aria-current="step"', html)
        self.assertIn(texts.HOME_STEP_CURRENT, html)


class DashboardStatsTests(AppTestCase):
    def test_painel_mostra_os_totais(self):
        self.create_active_user()
        self.register(email="pendente@gmail.com")  # fica por confirmar
        runner = self.app.test_cli_runner()
        runner.invoke(args=["create-admin", "--username", "gestor", "--password", "gestao-segura-1"])
        self.set_csrf()
        self.client.post("/auth/entrar", data={"csrf_token": CSRF_TOKEN, "email": "gestor", "password": "gestao-segura-1"})
        html = self.client.get("/gestao/").get_data(as_text=True)
        self.assertIn('data-contar="1"', html)  # um aluno ativo, uma conta por confirmar, um administrador
        self.assertEqual(html.count('data-contar="1"'), 3)
        self.assertNotIn("pendente@gmail.com", html)  # só totais, nunca dados de um aluno


class DetailsTests(AppTestCase):
    def test_pagina_nao_encontrada_mostra_o_caminho_perdido(self):
        response = self.client.get("/nao-existe")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn('class="perdido"', html)
        self.assertIn(texts.NOT_FOUND_HINT, html)

    def test_icone_e_script_sao_ficheiros_proprios(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('href="/static/favicon.svg"', html)
        self.assertIn('src="/static/app.js"', html)
        for ficheiro in ("/static/app.js", "/static/favicon.svg"):
            response = self.client.get(ficheiro)
            self.assertEqual(response.status_code, 200)
            response.close()

    def test_registo_tem_as_regras_da_palavra_passe(self):
        html = self.client.get("/auth/registo").get_data(as_text=True)
        self.assertIn("data-regras", html)
        self.assertIn(texts.REGISTER_RULE_MATCH, html)
