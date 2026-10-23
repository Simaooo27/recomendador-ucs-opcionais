"""Plano de candidatura (protótipo de 23/10): contas, opções, avisos e páginas."""
import csv
import os
import tempfile
import unittest

from app import texts
from app.candidatura import services
from app.candidatura.calculos import (
    Notas, Situacao, chega_na_2a_fase, exames_que_abrem_portas, nota_de_exame, nota_necessaria, simular,
)
from app.catalogo.repository import Curso
from tests.base import CSRF_TOKEN, AppTestCase


def _curso(**campos) -> Curso:
    base = dict(
        codigo_instituicao="1107", codigo_curso="9694", curso="Ciência da Informação", instituicao="Universidade do Porto",
        unidade_organica="Faculdade de Letras", localidade="Porto", tipo_ensino="Público universitário",
        area="Ciência da Informação", vagas=46, ultimo_colocado="138,3", descricao="", saidas="", fonte="",
        provas=(("18",), ("11", "18")), peso_secundario=50, peso_provas=50, minimo_candidatura=95, minimo_provas=95,
    )
    base.update(campos)
    return Curso(**base)


class ContasTests(unittest.TestCase):
    def test_nota_de_candidatura_com_a_formula_do_curso(self):
        # 50% × 152 + 50% × 140 = 146,0; o último colocado teve 138,3.
        sim = simular(_curso(), Notas(15.2, {"18": 140}))
        self.assertEqual(sim.nota, 146.0)
        self.assertEqual(sim.diferenca, 7.7)
        self.assertIs(sim.situacao, Situacao.ACIMA)
        self.assertEqual(sim.conjunto, ("18",))

    def test_usa_o_conjunto_de_provas_que_da_a_nota_mais_alta(self):
        # Só Português: 145; Português e História (média 165): 50% × 150 + 50% × 165 = 157,5.
        sim = simular(_curso(), Notas(15.0, {"18": 140, "11": 190}))
        self.assertEqual(sim.conjunto, ("11", "18"))
        self.assertEqual(sim.nota, 157.5)

    def test_perto_e_abaixo_do_ultimo_colocado(self):
        self.assertIs(simular(_curso(), Notas(13.5, {"18": 140})).situacao, Situacao.PERTO)     # 137,5
        self.assertIs(simular(_curso(), Notas(12.0, {"18": 120})).situacao, Situacao.ABAIXO)    # 120,0

    def test_falta_prova_diz_qual_falta(self):
        sim = simular(_curso(provas=(("16", "07"),)), Notas(15.0, {"07": 150}))
        self.assertIs(sim.situacao, Situacao.FALTA_PROVA)
        self.assertEqual(sim.em_falta, ("16",))

    def test_matematica_e_matematica_a_contam_com_o_mesmo_exame(self):
        sim = simular(_curso(provas=(("16",),)), Notas(15.0, {"19": 150}))
        self.assertEqual(sim.nota, 150.0)

    def test_prova_abaixo_do_minimo_nao_conta(self):
        sim = simular(_curso(), Notas(18.0, {"18": 90}))
        self.assertIs(sim.situacao, Situacao.ABAIXO_DO_MINIMO)
        self.assertEqual(sim.abaixo_do_minimo, ("18",))
        self.assertFalse(sim.situacao.conta)

    def test_sem_notas_sem_regras_e_sem_referencia(self):
        self.assertIs(simular(_curso(), Notas()).situacao, Situacao.SEM_NOTAS)
        self.assertIs(simular(_curso(provas=()), Notas(15, {"18": 150})).situacao, Situacao.SEM_REGRAS)
        self.assertIs(simular(_curso(ultimo_colocado=None), Notas(15, {"18": 150})).situacao, Situacao.SEM_REFERENCIA)

    def test_exames_em_valores_ou_em_pontos(self):
        self.assertEqual(nota_de_exame("14,5"), 145.0)
        self.assertEqual(nota_de_exame("145"), 145.0)
        self.assertIsNone(nota_de_exame("abc"))


class QuantoPrecisaTests(unittest.TestCase):
    def test_nota_necessaria_para_chegar_ao_ultimo_colocado(self):
        # 138,3 = 50% × 152 + 50% × x  ->  x = 124,6 em Português (o conjunto mais fácil).
        nec = nota_necessaria(_curso(), Notas(15.2, {}))
        self.assertEqual((nec.pontos, nec.em_falta, nec.alvo), (124.6, ("18",), 138.3))
        self.assertTrue(nec.possivel and nec.alvo_e_o_ultimo)

    def test_conta_com_a_prova_ja_feita_do_conjunto(self):
        # História + Português: média das provas tem de ser 124,6; com 180 a História basta 69,2,
        # mas o mínimo de cada prova é 95.
        nec = nota_necessaria(_curso(provas=(("11", "18"),)), Notas(15.2, {"11": 180}))
        self.assertEqual((nec.pontos, nec.em_falta), (95.0, ("18",)))

    def test_avisa_quando_nem_200_chegam(self):
        nec = nota_necessaria(_curso(ultimo_colocado="190,0"), Notas(12.0, {}))
        self.assertFalse(nec.possivel)
        self.assertEqual(nec.maximo, 160.0)                # 50% × 120 + 50% × 200

    def test_sem_referencia_usa_a_nota_minima(self):
        nec = nota_necessaria(_curso(ultimo_colocado=None), Notas(12.0, {}))
        self.assertFalse(nec.alvo_e_o_ultimo)
        self.assertEqual(nec.alvo, 95.0)

    def test_sem_media_ou_com_tudo_feito_nao_ha_conta(self):
        self.assertIsNone(nota_necessaria(_curso(), Notas()))
        self.assertIsNone(nota_necessaria(_curso(provas=(("18",),)), Notas(15, {"18": 150})))


class TendenciaEProcuraTests(unittest.TestCase):
    def test_tendencia_compara_o_ano_mais_recente_com_o_mais_antigo(self):
        self.assertEqual(_curso(ultimo_colocado_2023="152,0", ultimo_colocado_2024="144,0").tendencia, "desce")
        self.assertEqual(_curso(ultimo_colocado_2023="130,0").tendencia, "sobe")
        self.assertEqual(_curso(ultimo_colocado_2024="137,0").tendencia, "estavel")
        self.assertIsNone(_curso().tendencia)                       # só um ano

    def test_procura(self):
        base = dict(vagas_1fase=46, candidatos=178)
        self.assertEqual(_curso(**base, candidatos_1opcao=20, colocados=46).procura, "pouca")
        self.assertEqual(_curso(**base, candidatos_1opcao=40, colocados=46).procura, "media")
        self.assertEqual(_curso(**base, candidatos_1opcao=90, colocados=46).procura, "muita")
        self.assertEqual(_curso(**base, candidatos_1opcao=90, colocados=30).procura, "sobraram")
        self.assertIsNone(_curso().procura)


class RecolhaDaTabelaTests(unittest.TestCase):
    def test_le_a_1a_fase_de_cada_ano_e_distingue_as_duas_linhas_em_1a_opcao(self):
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("recolher_dges", Path(__file__).resolve().parents[1] / "dados" / "recolher_dges.py")
        recolha = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(recolha)
        def linha(nome, *valores):
            return "<tr><th>" + nome + "</th>" + "".join(f"<td>{v}</td>" for v in valores) + "</tr>"
        pagina = (
            "<h2>Dados Estatísticos de Candidaturas Anteriores</h2><table>"
            '<tr><td></td><th colspan="2" class="th1">2023</th><th colspan="2" class="th1">2024</th><th colspan="2" class="th1">2025</th></tr>'
            + linha("Vagas", 46, 8, 46, 11, 46, 6) + linha("Candidatos", *[""] * 6) + linha("Candidatos", 331, 98, 200, 91, 178, 36)
            + linha("em 1ª Opção", 41, 16, 28, 14, 20, 7) + linha("Colocados", 46, 10, 47, 14, 46, 7)
            + linha("em 1ª Opção", 10, 1, 15, 2, 17, 5)
            + linha("Nota de Candidatura do Último Colocado pelo Contingente Geral", "152,0", "150,8", "144,0", "147,0", "138,3", "136,8")
            + "</table>"
        )
        dados = recolha._tendencia_e_procura(pagina)
        self.assertEqual(dados, {
            "ultimo_colocado_1fase_2023": "152,0", "ultimo_colocado_1fase_2024": "144,0",
            "vagas_1fase_2025": "46", "candidatos_1fase_2025": "178", "candidatos_1opcao_1fase_2025": "20",
            "colocados_1fase_2025": "46",
            # 2.ª fase de 2025 (plano B): vagas 6, colocados 7, último colocado 136,8
            "vagas_2fase_2025": "6", "colocados_2fase_2025": "7", "ultimo_colocado_2fase_2025": "136,8",
        })


class ExamesQueAbremPortasTests(unittest.TestCase):
    def test_escolhe_a_combinacao_que_serve_para_mais_cursos(self):
        a = _curso(codigo_instituicao="1", curso="A", provas=(("18",), ("11", "18")))
        b = _curso(codigo_instituicao="2", curso="B", provas=(("19", "18"),))
        c = _curso(codigo_instituicao="3", curso="C", provas=(("07", "19"),))
        melhor = exames_que_abrem_portas([a, b, c], Notas(15, {"18": 140}))[0]
        # Português + Matemática A abre A e B; para abrir os três seriam precisos 3 exames (07, 18, 19).
        self.assertEqual(melhor.provas, ("07", "18", "19"))
        self.assertEqual(len(melhor.abre), 3)
        self.assertEqual(melhor.ja_feitas, ("18",))
        seguinte = exames_que_abrem_portas([a, b, c], Notas(15, {}))[1]
        self.assertEqual((seguinte.provas, [x.curso for x in seguinte.nao_abre]), (("18", "19"), ["C"]))

    def test_matematica_16_e_19_contam_como_a_mesma(self):
        a = _curso(codigo_instituicao="1", provas=(("16",),))
        b = _curso(codigo_instituicao="2", provas=(("19",),))
        self.assertEqual(exames_que_abrem_portas([a, b], Notas())[0].provas, ("19",))

    def test_precisa_de_pelo_menos_dois_cursos_com_regras(self):
        self.assertEqual(exames_que_abrem_portas([_curso()], Notas()), [])


class PlanoBTests(unittest.TestCase):
    def test_chega_quando_a_nota_passa_o_ultimo_da_2a_fase(self):
        curso = _curso(ultimo_colocado="150,0", vagas_2fase=6, colocados_2fase=7, ultimo_colocado_2fase="140,0")
        self.assertIsNotNone(chega_na_2a_fase(curso, Notas(15.2, {"18": 140})))   # 146,0 ≥ 140,0
        self.assertIsNone(chega_na_2a_fase(curso, Notas(13.0, {"18": 140})))      # 135,0
        self.assertIsNone(chega_na_2a_fase(_curso(), Notas(15.2, {"18": 140})))   # sem vagas na 2.ª fase

    def test_sem_nota_da_2a_fase_so_conta_se_sobraram_vagas(self):
        sobraram = _curso(vagas_2fase=10, colocados_2fase=4)
        self.assertIsNotNone(chega_na_2a_fase(sobraram, Notas(12, {"18": 120})))
        self.assertIsNone(chega_na_2a_fase(_curso(vagas_2fase=10, colocados_2fase=10), Notas(12, {"18": 120})))


class AvisosTests(unittest.TestCase):
    def _lista(self, *cursos, notas=Notas(15.2, {"18": 140})):
        plano = services.Plano(notas, tuple(c.chave for c in cursos))
        return plano, services.opcoes(plano, cursos)

    def test_avisa_quando_nenhuma_opcao_e_segura_e_quando_ha_menos_de_6(self):
        dificil = _curso(codigo_instituicao="1", ultimo_colocado="170,0")
        plano, lista = self._lista(dificil)
        avisos = services.avisos(plano, lista)
        self.assertIn(texts.CANDIDATURA_AVISO_SEM_SEGURA, avisos)
        self.assertIn(texts.CANDIDATURA_AVISO_MENOS_DE_6.format(n=1, livres=5), avisos)

    def test_avisa_quando_a_opcao_mais_facil_esta_em_primeiro(self):
        facil = _curso(codigo_instituicao="1", curso="Fácil", ultimo_colocado="120,0")
        dificil = _curso(codigo_instituicao="2", ultimo_colocado="145,0")
        plano, lista = self._lista(facil, dificil)
        self.assertIn(texts.CANDIDATURA_AVISO_ORDEM.format(curso="Fácil"), services.avisos(plano, lista))
        plano, lista = self._lista(dificil, facil)
        self.assertNotIn(texts.CANDIDATURA_AVISO_ORDEM.format(curso="Fácil"), services.avisos(plano, lista))


_COLUNAS = [
    "instituicao", "unidade_organica", "tipo_ensino", "localidade", "codigo_instituicao_dges", "codigo_curso_dges",
    "curso", "area_optabem", "grau", "duracao_semestres", "ects", "vagas_2026", "ultimo_colocado_1fase_2025",
    "area_cnaef", "descricao", "saidas_profissionais", "fonte_dados_acesso", "fonte_descricao", "provas_ingresso",
    "peso_secundario", "peso_provas", "minimo_candidatura", "minimo_provas", "pre_requisitos",
    "ultimo_colocado_1fase_2023", "ultimo_colocado_1fase_2024", "vagas_1fase_2025", "candidatos_1fase_2025",
    "candidatos_1opcao_1fase_2025", "colocados_1fase_2025", "vagas_2fase_2025", "colocados_2fase_2025",
    "ultimo_colocado_2fase_2025",
]


def _linha(code, codc, curso, ultimo, provas="18|11+18", pre=""):
    return {
        "instituicao": f"Instituição {code}", "unidade_organica": "", "tipo_ensino": "Público universitário",
        "localidade": "Porto", "codigo_instituicao_dges": code, "codigo_curso_dges": codc, "curso": curso,
        "area_optabem": "Ciência da Informação", "grau": "Licenciatura (1.º ciclo)", "duracao_semestres": "6",
        "ects": "180", "vagas_2026": "40", "ultimo_colocado_1fase_2025": ultimo, "area_cnaef": "", "descricao": "",
        "saidas_profissionais": "", "fonte_dados_acesso": "https://www.dges.gov.pt/", "fonte_descricao": "",
        "provas_ingresso": provas, "peso_secundario": "50", "peso_provas": "50", "minimo_candidatura": "95",
        "minimo_provas": "95", "pre_requisitos": pre,
        "ultimo_colocado_1fase_2023": "130,0", "ultimo_colocado_1fase_2024": "", "vagas_1fase_2025": "40",
        "candidatos_1fase_2025": "200", "candidatos_1opcao_1fase_2025": "80", "colocados_1fase_2025": "40",
        "vagas_2fase_2025": "5", "colocados_2fase_2025": "5", "ultimo_colocado_2fase_2025": "125,0",
    }


class PaginasDoPlanoTests(AppTestCase):
    def setUp(self):
        self._dados = tempfile.TemporaryDirectory()
        caminho = os.path.join(self._dados.name, "catalogo-cursos.csv")
        with open(caminho, "w", encoding="utf-8-sig", newline="") as ficheiro:
            escritor = csv.DictWriter(ficheiro, fieldnames=_COLUNAS)
            escritor.writeheader()
            escritor.writerow(_linha("0001", "9000", "Curso Acessível", "120,0"))
            escritor.writerow(_linha("0002", "9000", "Curso Disputado", "170,0"))
            escritor.writerow(_linha("0003", "9000", "Curso Vizinho", "130,0"))
            escritor.writerow(_linha("0004", "9000", "Curso Sem Regras", "", provas=""))
        with open(os.path.join(self._dados.name, "provas-ingresso.csv"), "w", encoding="utf-8-sig", newline="") as ficheiro:
            ficheiro.write("codigo,nome\n11,História\n16,Matemática\n18,Português\n19,Matemática A\n")
        self.config_overrides = {"CATALOGO_CSV": caminho}
        super().setUp()
        self.create_active_user()
        self.login()

    def tearDown(self):
        super().tearDown()
        self._dados.cleanup()

    def _post(self, caminho, **dados):
        self.set_csrf()
        return self.client.post(caminho, data={"csrf_token": CSRF_TOKEN, **dados})

    def test_e_preciso_ter_sessao(self):
        self.logout()
        self.assertEqual(self.client.get("/candidatura/").status_code, 302)

    def test_notas_invalidas_nao_sao_guardadas(self):
        response = self._post("/candidatura/notas", media="25", exame_18="abc")
        self.assertEqual(response.status_code, 422)
        html = response.get_data(as_text=True)
        self.assertIn(texts.CANDIDATURA_ERRO_MEDIA, html)
        self.assertIn(texts.CANDIDATURA_ERRO_EXAME, html)

    def test_o_formulario_mostra_matematica_a_uma_so_vez(self):
        html = self.client.get("/candidatura/notas").get_data(as_text=True)
        self.assertIn('name="exame_19"', html)
        self.assertNotIn('name="exame_16"', html)

    def test_percurso_completo_notas_juntar_ordenar_e_retirar(self):
        self.assertEqual(self._post("/candidatura/notas", media="15,2", exame_18="14").status_code, 302)
        self._post("/candidatura/juntar/0002-9000")
        self._post("/candidatura/juntar/0001-9000")
        html = self.client.get("/candidatura/").get_data(as_text=True)
        self.assertLess(html.index("Curso Disputado"), html.index("Curso Acessível"))
        self.assertIn("146,0", html)                      # 50% × 152 + 50% × 140
        self.assertIn("Curso Vizinho", html)              # sugestão da mesma área onde fica acima

        self._post("/candidatura/subir/0001-9000")
        html = self.client.get("/candidatura/").get_data(as_text=True)
        self.assertLess(html.index('data-chave="0001-9000"'), html.index('data-chave="0002-9000"'))

        self._post("/candidatura/retirar/0001-9000")
        self.assertNotIn('data-chave="0001-9000"', self.client.get("/candidatura/").get_data(as_text=True))

    def test_no_maximo_6_opcoes_e_sem_repetidos(self):
        with self.app.app_context():
            from app.db import get_db
            user_id = get_db().execute("SELECT id FROM users").fetchone()["id"]
            for i in range(6):
                services.juntar(get_db(), user_id, f"x-{i}")
            self.assertFalse(services.juntar(get_db(), user_id, "x-0"))
            with self.assertRaises(services.PlanoCheio):
                services.juntar(get_db(), user_id, "x-6")

    def test_curso_inexistente_da_404(self):
        self.assertEqual(self._post("/candidatura/juntar/nao-existe").status_code, 404)

    def test_a_ficha_mostra_as_condicoes_de_acesso_e_a_nota_do_aluno(self):
        self._post("/candidatura/notas", media="15,2", exame_18="140")
        html = self.client.get("/cursos/0001-9000").get_data(as_text=True)
        self.assertIn(texts.FICHA_ACESSO, html)
        self.assertIn("História + Português", html)
        self.assertIn("146,0", html)
        self.assertIn(texts.CANDIDATURA_JUNTAR, html)
        self.assertIn(texts.FICHA_SEM_ACESSO, self.client.get("/cursos/0004-9000").get_data(as_text=True))

    def test_a_ficha_mostra_tendencia_procura_e_quanto_precisa(self):
        self._post("/candidatura/notas", media="15,2")
        html = self.client.get("/cursos/0003-9000").get_data(as_text=True)    # 130,0 (2023) -> 130,0 (2025)
        self.assertIn(texts.FICHA_TENDENCIA_ESTAVEL, html)
        self.assertIn(texts.FICHA_PROCURA_MUITA, html)                          # 80 em 1.ª opção para 40 vagas
        self.assertIn(texts.FICHA_PRECISA_TITULO, html)
        self.assertIn("108,0 pontos", html)                                      # 130 = 76 + 50% × 108

    def test_partilhar_mostra_o_plano_sem_dados_pessoais_e_desligar_invalida(self):
        self._post("/candidatura/notas", media="15,2", exame_18="140")
        self._post("/candidatura/juntar/0001-9000")
        self._post("/candidatura/partilhar")
        import sqlite3
        connection = sqlite3.connect(self.db_path)
        codigo = connection.execute("SELECT partilha FROM planos_candidatura").fetchone()[0]
        connection.close()
        self.assertGreaterEqual(len(codigo), 20)
        self.assertIn(f"/candidatura/p/{codigo}", self.client.get("/candidatura/").get_data(as_text=True))

        self.logout()
        resposta = self.client.get(f"/candidatura/p/{codigo}")
        html = resposta.get_data(as_text=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(texts.PARTILHA_TITULO.format(nome="Ana"), html)
        self.assertIn("Curso Acessível", html)
        self.assertIn("146,0", html)
        self.assertNotIn("aluno@gmail.com", html)
        self.assertNotIn("15,2", html)                    # nem a média…
        self.assertNotIn("140,0", html)                   # …nem a nota do exame
        self.assertIn("noindex", html)
        self.assertEqual(resposta.headers["Referrer-Policy"], "no-referrer")

        self.login()
        self._post("/candidatura/deixar-de-partilhar")
        self.assertEqual(self.client.get(f"/candidatura/p/{codigo}").status_code, 404)

    def test_o_plano_mostra_exames_que_abrem_portas_e_plano_b(self):
        self._post("/candidatura/notas", media="15,2", exame_18="140")
        self._post("/candidatura/juntar/0002-9000")
        self._post("/candidatura/juntar/0001-9000")
        html = self.client.get("/candidatura/").get_data(as_text=True)
        self.assertIn(texts.EXAMES_TITULO, html)
        self.assertIn(texts.EXAMES_TODAS, html)
        exames = html[html.index(texts.EXAMES_TITULO):html.index(texts.PLANO_B_TITULO)]
        self.assertIn('<p class="combinacao-provas">Português</p>', exames)   # Português basta para os dois
        self.assertEqual(exames.count('class="cartao combinacao"'), 1)
        self.assertIn(texts.PLANO_B_TITULO, html)
        plano_b = html[html.index(texts.PLANO_B_TITULO):]
        self.assertIn("Curso Vizinho", plano_b)           # 146,0 ≥ 125,0 na 2.ª fase
        self.assertNotIn("Curso Disputado", plano_b)       # já está no plano

    def test_codigo_de_partilha_errado_da_404(self):
        self.assertEqual(self.client.get("/candidatura/p/nao-existe").status_code, 404)

    def test_partilhar_exige_csrf(self):
        self.client.post("/candidatura/partilhar", data={"csrf_token": "errado"})
        import sqlite3
        connection = sqlite3.connect(self.db_path)
        self.assertIsNone(connection.execute("SELECT partilha FROM planos_candidatura").fetchone())
        connection.close()

    def test_voltar_so_aceita_caminhos_do_proprio_site(self):
        response = self._post("/candidatura/juntar/0001-9000", voltar="//exemplo.com/")
        self.assertTrue(response.headers["Location"].endswith("/candidatura/"))

    def test_apagar_a_conta_apaga_o_plano(self):
        self._post("/candidatura/notas", media="15")
        self._post("/auth/conta/apagar", password="palavra-passe-1")
        import sqlite3
        connection = sqlite3.connect(self.db_path)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM planos_candidatura").fetchone()[0], 0)
        connection.close()


if __name__ == "__main__":
    unittest.main()
