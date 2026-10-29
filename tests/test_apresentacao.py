"""Página de apresentação, «O seu percurso», painel com números e detalhes de interação."""
from app import percurso, texts
from app.percurso import EstadoPercurso
from tests.base import CSRF_TOKEN, AppTestCase


def _location(response) -> str:
    return response.headers.get("Location", "")


class LandingPageTests(AppTestCase):
    def test_sem_sessao_mostra_a_apresentacao(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn(texts.LANDING_HOW_TITLE, html)
        self.assertIn(texts.LANDING_SEARCH_LABEL, html)
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

    def test_mostra_numeros_reais_do_catalogo(self):
        html = self.client.get("/").get_data(as_text=True)
        # Desde o visual calmo (29/10) os números já não contam até ao valor: aparecem logo.
        self.assertIn('<strong>30</strong> licenciaturas', html)
        self.assertIn('<strong>12</strong> instituições', html)


class CourseSearchTests(AppTestCase):
    """Pesquisa no catálogo real (app/catalogo), na página de apresentação."""

    def test_sem_termo_mostra_uma_amostra_de_cursos(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn(texts.LANDING_RESULTS_SAMPLE, html)
        self.assertEqual(html.count('class="curso" data-chave='), 6)

    def test_pesquisa_sem_javascript_com_q(self):
        html = self.client.get("/?q=coimbra").get_data(as_text=True)
        self.assertIn(texts.LANDING_RESULTS_FOUND.format(termo="coimbra"), html)
        self.assertEqual(html.count('class="curso" data-chave='), 3)  # Coimbra tem 3 cursos no catálogo
        self.assertNotIn("Universidade do Minho", html.split('id="lista-cursos"')[1].split("</ul>")[0])

    def test_pesquisa_ignora_acentos_e_maiusculas(self):
        dados = self.client.get("/cursos/pesquisa?q=CIENCIA informacao").get_json()
        self.assertGreater(dados["total"], 0)
        self.assertTrue(all("Informação" in c["curso"] or c["area"] == "Ciência da Informação" for c in dados["cursos"]))

    def test_todas_as_palavras_tem_de_aparecer(self):
        dados = self.client.get("/cursos/pesquisa?q=informatica porto").get_json()
        self.assertTrue(dados["cursos"])
        self.assertTrue(all(c["localidade"] == "Porto" or "Porto" in c["instituicao"] for c in dados["cursos"]))

    def test_sem_resultados_mostra_mensagem(self):
        html = self.client.get("/?q=medicina").get_data(as_text=True)
        self.assertIn(texts.LANDING_NO_RESULTS.format(termo="medicina"), html)
        self.assertNotIn('data-resultados-vazio hidden', html)

    def test_resposta_json_tem_os_campos_da_ficha(self):
        dados = self.client.get("/cursos/pesquisa?q=gestao").get_json()
        self.assertEqual(set(dados), {"termo", "total", "amostra", "cursos"})
        self.assertEqual(
            set(dados["cursos"][0]),
            {"curso", "instituicao", "unidade", "localidade", "area", "vagas", "ultimo_colocado", "fonte", "chave", "ficha"},
        )
        self.assertEqual(dados["cursos"][0]["ficha"], "/cursos/" + dados["cursos"][0]["chave"])   # US05
        self.assertTrue(dados["cursos"][0]["fonte"].startswith("https://www.dges.gov.pt/"))

    def test_termo_muito_longo_e_cortado(self):
        dados = self.client.get("/cursos/pesquisa?q=" + "a" * 500).get_json()
        self.assertEqual(len(dados["termo"]), 80)


class VisualCalmoTests(AppTestCase):
    """Visual calmo (29/10): sem tipos de letra descarregados, sem letra «escrita à mão» nem números a contar."""

    def test_as_paginas_nao_carregam_tipos_de_letra(self):
        for pagina in ("/", "/auth/entrar", "/auth/registo"):
            with self.subTest(pagina=pagina):
                html = self.client.get(pagina).get_data(as_text=True)
                self.assertNotIn("fonts/", html)
                self.assertNotIn("manuscrito", html)
                self.assertNotIn("data-contar", html)

    def test_o_estilo_nao_tem_font_face(self):
        css = self.client.get("/static/style.css").get_data(as_text=True)
        self.assertNotIn("@font-face", css)

    def test_o_inicio_destaca_o_proximo_passo_com_um_botao(self):
        self.create_active_user()
        self.login()
        html = self.client.get("/inicio").get_data(as_text=True)
        destaque = html.split('class="inicio-destaque"')[1].split('class="faixa')[0]
        self.assertIn(texts.HOME_PASSO_DE.format(numero=2, total=4), destaque)
        self.assertIn(texts.HOME_PATH_STEPS[1]["titulo"], destaque)
        self.assertIn('href="/orientacao/"', destaque)


class PathTimelineTests(AppTestCase):
    """«O seu percurso» na página inicial do aluno (padrão State, app/percurso/__init__.py)."""

    def test_sem_curso_o_proximo_passo_e_o_questionario(self):
        passos = percurso.passos(EstadoPercurso.SEM_CURSO)
        self.assertEqual([p.situacao for p in passos], ["feito", "atual", "depois", "depois"])
        self.assertEqual(passos[1].titulo, texts.HOME_PATH_STEPS[1]["titulo"])

    def test_cada_estado_avanca_o_passo_atual(self):
        atuais = [
            [p.situacao for p in percurso.passos(estado)].index("atual")
            for estado in (EstadoPercurso.SEM_CURSO, EstadoPercurso.A_ESCOLHER_CURSO)
        ]
        self.assertEqual(atuais, [1, 2])

    def test_com_curso_o_proximo_passo_e_o_plano_de_candidatura(self):
        # Protótipo de 23/10: depois de escolher o curso, prepara-se a candidatura.
        passos = percurso.passos(EstadoPercurso.COM_CURSO)
        self.assertEqual([p.situacao for p in passos], ["feito", "feito", "feito", "atual"])
        self.assertEqual(passos[3].acao, (texts.HOME_ACTION_CANDIDATURA, "candidatura.plano"))

    def test_nao_ha_referencias_a_opcionais(self):
        # Decisão dos PO (22/10): nesta release o site não fala de opcionais.
        for pagina in ("/", "/privacidade", "/auth/entrar"):
            html = self.client.get(pagina).get_data(as_text=True).lower()
            self.assertNotIn("opcionais", html, pagina)
        self.create_active_user()
        self.login()
        self.assertNotIn("opcionais", self.client.get("/inicio").get_data(as_text=True).lower())

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
        # Um aluno ativo, uma conta por confirmar e um administrador.
        self.assertEqual(html.count('<dd>1</dd>'), 3)
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


class MenuDaApresentacaoTests(AppTestCase):
    """Decisão do PO (22/10): a barra do topo fica presa ao topo e é o único sítio da
    apresentação com «Entrar» e «Criar conta» (antes havia 2 e 3 de cada)."""

    def test_entrar_e_criar_conta_aparecem_uma_so_vez(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertEqual(html.count('href="/auth/entrar"'), 1)
        self.assertEqual(html.count('href="/auth/registo"'), 1)

    def test_a_barra_tem_as_seccoes_da_pagina(self):
        html = self.client.get("/").get_data(as_text=True)
        for destino in ('href="/cursos/"', 'href="/#como-funciona"', 'href="/#para-quem"'):
            self.assertIn(destino, html)
        self.assertIn('id="como-funciona"', html)
        self.assertIn('id="para-quem"', html)

    def test_a_barra_do_topo_fica_presa(self):
        from pathlib import Path
        import re

        css = (Path(self.app.static_folder) / "style.css").read_text(encoding="utf-8")
        regra = re.search(r"\.site-header \{([^}]*)\}", css).group(1)
        self.assertIn("position: sticky", regra)
        self.assertIn("top: 0", regra)
