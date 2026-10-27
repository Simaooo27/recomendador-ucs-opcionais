"""US04: catálogo completo da DGES (dados/recolher_dges.py) e filtro por área no assistente."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

from app.catalogo.repository import Curso
from app.llm.adaptadores import LLMFalso
from app.llm import Mensagem, RespostaInvalida
from app.orientacao import conversa

RAIZ = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("recolher_dges", RAIZ / "dados" / "recolher_dges.py")
recolha = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(recolha)

# Página de curso com a mesma estrutura das da DGES (só as partes que o script lê).
PAGINA = """
<div class="cab1">Administra&ccedil;&atilde;o P&uacute;blica</div>
<div class="cab2">Universidade de Coimbra - Faculdade de Direito</div>
Pátio da Universidade<br>3004-528 COIMBRA<br>
<h2>Características do par Instituição/Curso</h2>Código: 0502/9002<br>Grau: Licenciatura - 1º ciclo<br>
Área CNAEF: 345 Gestão e Administração<br>Duração: 3 Anos<br>ECTS: 180<br>
Tipo de Ensino: Ensino Superior Público Universitário<br>Concurso: Nacional<br>Vagas para 2026-2027: 41<br>
<th colspan="2" class="th1">2024</th><th colspan="2" class="th1">2025</th>
<th class="tlab lineorange">Nota de Candidatura do Último Colocado pelo Contingente Geral</th>
<td class="tvag">150,1</td><td class="tvag">149,0</td><td class="tvag">146,3</td><td class="tvag">140,0</td></tr>
"""


class LeituraDaPaginaTests(unittest.TestCase):
    def setUp(self):
        self.linha = recolha.ler_curso(PAGINA, "9002", "0502")

    def test_le_os_campos_da_ficha(self):
        self.assertEqual(self.linha["curso"], "Administração Pública")
        self.assertEqual((self.linha["instituicao"], self.linha["unidade_organica"]), ("Universidade de Coimbra", "Faculdade de Direito"))
        self.assertEqual(self.linha["localidade"], "Coimbra")
        self.assertEqual(self.linha["tipo_ensino"], "Público universitário")
        self.assertEqual(self.linha["vagas_2026"], "41")
        self.assertEqual(self.linha["duracao_semestres"], "6")   # «3 Anos»
        self.assertEqual(self.linha["area_optabem"], "Gestão")

    def test_nota_e_a_da_1a_fase_do_ano_mais_recente(self):
        self.assertEqual(self.linha["ultimo_colocado_1fase_2025"], "146,3")

    def test_privado_sem_nota(self):
        privada = PAGINA.replace("Ensino Superior Público Universitário", "Ensino Superior Universitário")
        privada = privada.split("<th colspan")[0]
        linha = recolha.ler_curso(privada, "9002", "0502")
        self.assertEqual(linha["tipo_ensino"], "Privado universitário")
        self.assertEqual(linha["ultimo_colocado_1fase_2025"], "")

    def test_areas_com_regras_pelo_nome(self):
        self.assertEqual(recolha._area("Engenharia Informática", "523 Eletrónica e Automação"), "Informática")
        self.assertEqual(recolha._area("Gestão de Informação", "345 Gestão e Administração"), "Ciência da Informação")
        self.assertEqual(recolha._area("Enfermagem", "723 Enfermagem"), "Saúde")

    def test_nomes_de_instituicoes(self):
        self.assertEqual(recolha._instituicao("ISCTE - Instituto Universitário de Lisboa"), ("Iscte - Instituto Universitário de Lisboa", ""))
        self.assertEqual(recolha._instituicao("Universidade da Maia"), ("Universidade da Maia", ""))

    def test_localidade_com_hifen(self):
        self.assertEqual(recolha._localidade("Rua X<br>6060-182 IDANHA-A-NOVA<br>"), "Idanha-a-Nova")


def _curso(n: int, area: str, localidade: str = "Lisboa", descricao: str = "") -> Curso:
    return Curso(f"{n:04d}", "9000", f"Curso {n}", "Instituição", "", localidade, "Público universitário", area,
                 100 - n % 50, None, descricao, "", "https://exemplo")


CATALOGO_GRANDE = [_curso(i, "Saúde" if i % 2 else "Artes", "Porto" if i % 7 == 0 else "Lisboa", "desc" if i < 5 else "")
                   for i in range(200)]


def _areas(*areas, localidades=()):
    return json.dumps({"tipo": "areas", "areas": list(areas), "localidades": list(localidades)})


def _sugestao(*ids):
    return json.dumps({"tipo": "sugestao", "texto": "x", "cursos": [{"id": i, "explicacao": "y"} for i in ids]})


class FiltroPorAreaTests(unittest.TestCase):
    """Acima de MAX_CURSOS_DIRETO cursos, o LLM recebe só as áreas e depois só os cursos delas."""

    def test_as_perguntas_levam_so_as_areas(self):
        llm = LLMFalso([json.dumps({"tipo": "pergunta", "texto": "Do que gosta?"})])
        passo = conversa.proximo_passo(llm, CATALOGO_GRANDE, [])
        self.assertIsInstance(passo, conversa.Pergunta)
        instrucoes = llm.pedidos[0][0]
        self.assertIn("- Saúde (100 cursos)", instrucoes)
        self.assertNotIn("Curso 1 |", instrucoes)   # nenhum curso nas instruções

    def test_as_areas_levam_a_um_segundo_pedido_so_com_esses_cursos(self):
        saude = [c for c in CATALOGO_GRANDE if c.area == "Saúde"]
        llm = LLMFalso([_areas("Saúde"), _sugestao(saude[0].chave, saude[1].chave)])
        passo = conversa.proximo_passo(llm, CATALOGO_GRANDE, [Mensagem("utilizador", "Gosto de ajudar pessoas")])
        self.assertIsInstance(passo, conversa.Sugestao)
        self.assertEqual(len(passo.cursos), 2)
        segunda = llm.pedidos[1][0]
        self.assertIn(saude[0].chave, segunda)
        self.assertNotIn("| Artes |", segunda)
        self.assertLessEqual(segunda.count("\n0"), conversa.MAX_CURSOS_ENVIADOS + 5)

    def test_cursos_de_outra_area_sao_descartados(self):
        artes = next(c for c in CATALOGO_GRANDE if c.area == "Artes")
        llm = LLMFalso([_areas("Saúde"), _sugestao(artes.chave)])
        passo = conversa.proximo_passo(llm, CATALOGO_GRANDE, [Mensagem("utilizador", "x")])
        self.assertEqual(passo.cursos, ())
        self.assertEqual(passo.descartados, (artes.chave,))

    def test_ordem_descricao_localidade_vagas(self):
        escolhidos = conversa.cursos_das_areas(CATALOGO_GRANDE, ["Saúde"], ["porto"])
        self.assertLessEqual(len(escolhidos), conversa.MAX_CURSOS_ENVIADOS)
        com_descricao = [c for c in escolhidos if c.descricao]
        self.assertEqual(escolhidos[:len(com_descricao)], com_descricao)
        seguintes = escolhidos[len(com_descricao):]
        self.assertEqual(seguintes[0].localidade, "Porto")

    def test_area_inventada_fica_com_os_cursos_com_descricao(self):
        escolhidos = conversa.cursos_das_areas(CATALOGO_GRANDE, ["Medicina em Harvard"])
        self.assertTrue(escolhidos)
        self.assertTrue(all(c.descricao for c in escolhidos))

    def test_sugestao_sem_areas_e_rejeitada(self):
        llm = LLMFalso([_sugestao("0001-9000")])
        with self.assertRaises(RespostaInvalida):
            conversa.proximo_passo(llm, CATALOGO_GRANDE, [Mensagem("utilizador", "x")])

    def test_limite_de_perguntas_pede_as_areas(self):
        llm = LLMFalso([json.dumps({"tipo": "pergunta", "texto": "mais uma?"})])
        respostas = [Mensagem("utilizador", "r")] * conversa.LIMITE_PERGUNTAS
        with self.assertRaises(RespostaInvalida):
            conversa.proximo_passo(llm, CATALOGO_GRANDE, respostas)
        self.assertIn("«areas»", llm.pedidos[0][0])

    def test_catalogo_pequeno_continua_como_antes(self):
        pequeno = CATALOGO_GRANDE[: conversa.MAX_CURSOS_DIRETO]
        llm = LLMFalso([_sugestao(pequeno[0].chave, pequeno[1].chave)])
        passo = conversa.proximo_passo(llm, pequeno, [Mensagem("utilizador", "x")])
        self.assertEqual(len(passo.cursos), 2)
        self.assertEqual(len(llm.pedidos), 1)
        self.assertIn("Curso 1 |", llm.pedidos[0][0])

    def test_llm_falso_simula_o_filtro(self):
        llm = LLMFalso()
        passo = conversa.proximo_passo(llm, CATALOGO_GRANDE, [Mensagem("utilizador", "a"), Mensagem("assistente", "b"), Mensagem("utilizador", "c")])
        self.assertIsInstance(passo, conversa.Sugestao)
        self.assertEqual(len(llm.pedidos), 2)


PAGINAS_GUARDADAS = sorted((RAIZ / "dados" / "dges_html" / "cursos").glob("*.html"))


@unittest.skipUnless(PAGINAS_GUARDADAS, "sem páginas da DGES guardadas em dados/dges_html/")
class CondicoesDeAcessoTests(unittest.TestCase):
    """US33: as condições de acesso lidas das páginas da DGES são as que estão no catálogo (27/10)."""

    @classmethod
    def setUpClass(cls):
        import csv
        with open(RAIZ / "dados" / "catalogo-cursos.csv", encoding="utf-8-sig", newline="") as ficheiro:
            cls.catalogo = {(l["codigo_instituicao_dges"], l["codigo_curso_dges"]): l for l in csv.DictReader(ficheiro)}

    def _ler(self, nome: str) -> dict[str, str]:
        codc, code = nome.removesuffix(".html").split("-")
        pagina = (RAIZ / "dados" / "dges_html" / "cursos" / nome).read_text(encoding="latin-1")   # como em processar()
        return recolha.ler_curso(pagina, codc, code)

    def test_conjuntos_alternativos_formula_e_minimos(self):
        if not (RAIZ / "dados" / "dges_html" / "cursos" / "8093-3062.html").exists():
            self.skipTest("página de exemplo não guardada")
        linha = self._ler("8093-3062.html")      # Animação Socioeducativa, Politécnico de Coimbra
        conjuntos = linha["provas_ingresso"].split("|")
        self.assertIn("17+18", conjuntos)          # um conjunto com duas provas
        self.assertIn("09", conjuntos)             # e um conjunto de uma só prova
        self.assertEqual((linha["peso_secundario"], linha["peso_provas"]), ("50", "50"))
        self.assertEqual((linha["minimo_candidatura"], linha["minimo_provas"]), ("95", "95"))

    def test_todas_as_paginas_guardadas_dao_as_condicoes_do_catalogo(self):
        campos = ("provas_ingresso", "peso_secundario", "peso_provas", "minimo_candidatura", "minimo_provas", "pre_requisitos")
        for caminho in PAGINAS_GUARDADAS:
            codc, code = caminho.stem.split("-")
            esperado = self.catalogo.get((code, codc))
            if esperado is None:
                continue
            with self.subTest(pagina=caminho.name):
                linha = self._ler(caminho.name)
                self.assertEqual({c: linha[c] for c in campos}, {c: esperado[c] for c in campos})
