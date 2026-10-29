"""US39: corrigir e esconder cursos do catálogo, na área de gestão."""
from __future__ import annotations

import csv
import os
import re
import shutil
import sqlite3
import tempfile
from html import unescape

from app import texts
from app.catalogo import repository as catalogo_repository
from app.catalogo import services as catalogo
from app.config import default_config
from tests.base import CSRF_TOKEN, VALID_EMAIL, AppTestCase
from tests.test_gestao import ADMIN, GestaoTestCase

# Um curso com descrição e saídas da DGES, para comparar com as correções.
CURSO = next(c for c in catalogo_repository.todos(default_config()["CATALOGO_CSV"]) if c.descricao and c.saidas)
DESCRICAO_NOVA = "Curso corrigido pela gestão: forma profissionais da informação."


class CatalogoGestaoTestCase(GestaoTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cli_create()
        self.admin_login()

    def guardar(self, chave=CURSO.chave, client=None, **campos):
        dados = {"descricao": "", "saidas": "", **campos}
        if dados.pop("escondido", False):
            dados["escondido"] = "on"
        client = client or self.client
        self.set_csrf(client)
        return client.post(f"/gestao/cursos/{chave}", data={"csrf_token": CSRF_TOKEN, **dados})

    def historico(self, chave=CURSO.chave) -> list[tuple]:
        ligacao = sqlite3.connect(self.db_path)
        try:
            return ligacao.execute(
                "SELECT alteracao, alterado_por, alterado_em FROM historico_catalogo WHERE curso_chave = ? ORDER BY id", (chave,)
            ).fetchall()
        finally:
            ligacao.close()

    def correcoes(self) -> int:
        ligacao = sqlite3.connect(self.db_path)
        try:
            return ligacao.execute("SELECT COUNT(*) FROM correcoes_cursos").fetchone()[0]
        finally:
            ligacao.close()

    def ficha(self, client=None):
        return (client or self.app.test_client()).get(f"/cursos/{CURSO.chave}")


class SoNaGestaoTests(CatalogoGestaoTestCase):
    """Critério: só na área de gestão."""

    def test_sem_sessao_e_alunos_nao_entram(self):
        self.create_active_user()
        aluno = self.app.test_client()
        self.login(aluno)
        for cliente in (self.app.test_client(), aluno):
            for url in ("/gestao/cursos", f"/gestao/cursos/{CURSO.chave}"):
                with self.subTest(url=url):
                    response = cliente.get(url)
                    self.assertEqual(response.status_code, 302)
                    self.assertTrue(response.headers["Location"].endswith("/auth/entrar"))
            response = self.guardar(client=cliente, descricao=DESCRICAO_NOVA)
            self.assertEqual(response.status_code, 302)
        self.assertEqual(self.correcoes(), 0)

    def test_sem_csrf_e_recusado(self):
        response = self.client.post(f"/gestao/cursos/{CURSO.chave}", data={"descricao": DESCRICAO_NOVA})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.correcoes(), 0)

    def test_a_gestao_tem_a_ligacao_para_o_catalogo(self):
        html = self.client.get("/gestao/").get_data(as_text=True)
        self.assertIn('href="/gestao/cursos"', html)

    def test_lista_e_procura_os_cursos(self):
        html = self.client.get("/gestao/cursos").get_data(as_text=True)
        self.assertIn(f'href="/gestao/cursos/{CURSO.chave}"', html)
        procura = self.client.get("/gestao/cursos", query_string={"q": CURSO.curso}).get_data(as_text=True)
        self.assertIn(CURSO.chave, procura)
        nada = self.client.get("/gestao/cursos", query_string={"q": "zzzzinexistente"}).get_data(as_text=True)
        self.assertIn(texts.ADMIN_CURSOS_VAZIO, nada)

    def test_curso_inexistente_da_404(self):
        self.assertEqual(self.client.get("/gestao/cursos/0000-XXXX").status_code, 404)
        self.assertEqual(self.guardar(chave="0000-XXXX", descricao=DESCRICAO_NOVA).status_code, 404)


class CorrigirTests(CatalogoGestaoTestCase):
    def test_corrigir_a_descricao_muda_a_ficha_e_o_catalogo_da_aplicacao(self):
        response = self.guardar(descricao=DESCRICAO_NOVA)
        self.assertEqual(response.status_code, 302)
        self.assertIn(DESCRICAO_NOVA, self.ficha().get_data(as_text=True))
        with self.app.app_context():
            curso = catalogo.por_chave(self.app.config, CURSO.chave)   # o mesmo que a conversa e o plano usam
        self.assertEqual(curso.descricao, DESCRICAO_NOVA)
        self.assertEqual(curso.saidas, CURSO.saidas)   # o que não se corrigiu fica igual

    def test_saidas_uma_por_linha(self):
        self.guardar(saidas="Bibliotecário\n  arquivista ;Gestor de conteúdos\n\n")
        with self.app.app_context():
            curso = catalogo.por_chave(self.app.config, CURSO.chave)
        self.assertEqual(curso.saidas, "Bibliotecário; arquivista; Gestor de conteúdos")
        html = self.ficha().get_data(as_text=True)
        self.assertIn("Gestor de conteúdos", html)

    def test_guardar_o_formulario_como_vem_so_muda_o_que_se_editou(self):
        """O formulário vem preenchido com o texto atual; mudar só a descrição não pode corrigir as saídas."""
        html = self.client.get(f"/gestao/cursos/{CURSO.chave}").get_data(as_text=True)
        saidas = re.search(r'<textarea id="saidas"[^>]*>(.*?)</textarea>', html, re.S).group(1)
        self.guardar(descricao=DESCRICAO_NOVA, saidas=unescape(saidas))
        self.assertEqual([h[0] for h in self.historico()], ["descricao"])

    def test_campo_vazio_ou_igual_ao_da_dges_nao_e_correcao(self):
        self.guardar(descricao=CURSO.descricao, saidas="")
        self.assertEqual(self.correcoes(), 0)
        self.assertEqual(self.historico(), [])

    def test_texto_demasiado_longo_e_recusado(self):
        response = self.guardar(descricao="x" * 3001)
        self.assertEqual(response.status_code, 422)
        self.assertIn(texts.ADMIN_CURSO_ERRO_LONGO.format(maximo=3000), response.get_data(as_text=True))
        self.assertEqual(self.correcoes(), 0)

    def test_o_texto_e_mostrado_sem_html(self):
        self.guardar(descricao="<script>alert(1)</script> Curso")
        html = self.ficha().get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)


class EsconderTests(CatalogoGestaoTestCase):
    def test_um_curso_escondido_desaparece_para_os_alunos(self):
        self.guardar(escondido=True)
        self.assertEqual(self.ficha().status_code, 404)
        visitante = self.app.test_client()
        self.assertNotIn(CURSO.chave, visitante.get("/cursos/", query_string={"q": CURSO.curso}).get_data(as_text=True))
        with self.app.app_context():
            self.assertNotIn(CURSO.chave, [c.chave for c in catalogo.cursos(self.app.config)])

    def test_continua_na_gestao_assinalado(self):
        self.guardar(escondido=True)
        html = self.client.get("/gestao/cursos", query_string={"mostrar": "escondidos"}).get_data(as_text=True)
        self.assertIn(CURSO.chave, html)
        self.assertIn(texts.ADMIN_CURSO_ESTADO_ESCONDIDO, html)
        self.assertEqual(self.client.get(f"/gestao/cursos/{CURSO.chave}").status_code, 200)

    def test_voltar_a_mostrar(self):
        self.guardar(escondido=True)
        self.guardar(escondido=False)
        self.assertEqual(self.ficha().status_code, 200)
        self.assertEqual(self.correcoes(), 0)
        self.assertEqual([h[0] for h in self.historico()], ["escondido", "visivel"])


class PorCimaDaDgesTests(AppTestCase):
    """Critério: as correções ficam na base de dados, por cima dos dados da DGES (a recolha seguinte não as apaga)."""

    def setUp(self) -> None:
        self._pasta = tempfile.TemporaryDirectory()
        self.csv = os.path.join(self._pasta.name, "catalogo-cursos.csv")
        shutil.copy(default_config()["CATALOGO_CSV"], self.csv)
        self.config_overrides = {"CATALOGO_CSV": self.csv}
        super().setUp()
        runner = self.app.test_cli_runner()
        runner.invoke(args=["create-admin", "--username", ADMIN, "--password", "gestao-segura-1"])
        self.set_csrf()
        self.client.post("/auth/entrar", data={"csrf_token": CSRF_TOKEN, "email": ADMIN, "password": "gestao-segura-1"})

    def tearDown(self) -> None:
        super().tearDown()
        self._pasta.cleanup()

    def _nova_recolha(self, descricao: str) -> None:
        """Simula a recolha seguinte da DGES: o CSV é reescrito, com outra descrição para o curso."""
        with open(self.csv, encoding="utf-8-sig", newline="") as ficheiro:
            leitor = csv.DictReader(ficheiro)
            colunas, linhas = leitor.fieldnames, list(leitor)
        for linha in linhas:
            if f"{linha['codigo_instituicao_dges']}-{linha['codigo_curso_dges']}" == CURSO.chave:
                linha["descricao"] = descricao
        with open(self.csv, "w", encoding="utf-8-sig", newline="") as ficheiro:
            escritor = csv.DictWriter(ficheiro, fieldnames=colunas)
            escritor.writeheader()
            escritor.writerows(linhas)
        os.utime(self.csv, (os.path.getmtime(self.csv) + 5,) * 2)   # o catálogo relê o ficheiro quando ele muda

    def test_a_correcao_sobrevive_a_uma_recolha_nova(self):
        self.set_csrf()
        self.client.post(f"/gestao/cursos/{CURSO.chave}", data={"csrf_token": CSRF_TOKEN, "descricao": DESCRICAO_NOVA, "saidas": ""})
        self._nova_recolha("Texto novo vindo da DGES.")
        html = self.app.test_client().get(f"/cursos/{CURSO.chave}").get_data(as_text=True)
        self.assertIn(DESCRICAO_NOVA, html)
        self.assertNotIn("Texto novo vindo da DGES.", html)

    def test_repor_mostra_o_texto_da_recolha_nova(self):
        self.set_csrf()
        self.client.post(f"/gestao/cursos/{CURSO.chave}", data={"csrf_token": CSRF_TOKEN, "descricao": DESCRICAO_NOVA, "saidas": ""})
        self._nova_recolha("Texto novo vindo da DGES.")
        self.set_csrf()
        response = self.client.post(f"/gestao/cursos/{CURSO.chave}/repor", data={"csrf_token": CSRF_TOKEN})
        self.assertEqual(response.status_code, 302)
        self.assertIn("Texto novo vindo da DGES.", self.app.test_client().get(f"/cursos/{CURSO.chave}").get_data(as_text=True))


class RegistoTests(CatalogoGestaoTestCase):
    """Critério: fica registado quem alterou e quando."""

    def test_regista_o_administrador_e_a_hora(self):
        self.guardar(descricao=DESCRICAO_NOVA)
        [(alteracao, por, em)] = self.historico()
        self.assertEqual((alteracao, por), ("descricao", ADMIN))
        self.assertRegex(em, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

    def test_a_pagina_do_curso_mostra_o_historico(self):
        self.guardar(descricao=DESCRICAO_NOVA, saidas="Arquivista")
        html = self.client.get(f"/gestao/cursos/{CURSO.chave}").get_data(as_text=True)
        self.assertIn(f"{texts.ADMIN_CURSO_O_QUE_DESCRICAO}, {texts.ADMIN_CURSO_O_QUE_SAIDAS}, por {ADMIN}", html)
        lista = self.client.get("/gestao/cursos", query_string={"mostrar": "corrigidos"}).get_data(as_text=True)
        self.assertIn(ADMIN, lista)

    def test_guardar_sem_mudar_nada_nao_regista(self):
        self.guardar(descricao=DESCRICAO_NOVA)
        response = self.guardar(descricao=DESCRICAO_NOVA)
        self.assertEqual(len(self.historico()), 1)
        self.assertIn(texts.ADMIN_CURSO_NADA_MUDOU, self.client.get(response.headers["Location"]).get_data(as_text=True))

    def test_repor_tambem_fica_registado(self):
        self.guardar(descricao=DESCRICAO_NOVA)
        self.set_csrf()
        self.client.post(f"/gestao/cursos/{CURSO.chave}/repor", data={"csrf_token": CSRF_TOKEN})
        self.assertEqual([h[0] for h in self.historico()], ["descricao", "reposto"])
        self.assertEqual(self.correcoes(), 0)

    def test_o_registo_fica_mesmo_se_o_administrador_for_removido(self):
        self.guardar(descricao=DESCRICAO_NOVA)
        ligacao = sqlite3.connect(self.db_path)
        try:
            ligacao.execute("DELETE FROM admins")
            ligacao.commit()
        finally:
            ligacao.close()
        self.assertEqual(self.historico()[0][1], ADMIN)


class SemDadosDosAlunosTests(CatalogoGestaoTestCase):
    """Critério: sem acesso aos dados dos alunos."""

    def test_as_paginas_do_catalogo_nao_mostram_dados_de_alunos(self):
        self.create_active_user()
        self.guardar(descricao=DESCRICAO_NOVA)
        for url in ("/gestao/cursos", f"/gestao/cursos/{CURSO.chave}", "/gestao/cursos?mostrar=corrigidos"):
            with self.subTest(url=url):
                self.assertNotIn(VALID_EMAIL, self.client.get(url).get_data(as_text=True))

    def test_as_tabelas_das_correcoes_nao_tem_ligacao_aos_alunos(self):
        ligacao = sqlite3.connect(self.db_path)
        try:
            for tabela in ("correcoes_cursos", "historico_catalogo"):
                with self.subTest(tabela=tabela):
                    colunas = {linha[1] for linha in ligacao.execute(f"PRAGMA table_info({tabela})")}
                    self.assertFalse(colunas & {"user_id", "email", "nome"})
                    self.assertEqual(ligacao.execute(f"PRAGMA foreign_key_list({tabela})").fetchall(), [])
        finally:
            ligacao.close()

    def test_o_formulario_so_altera_descricao_saidas_e_visibilidade(self):
        """Campos a mais no pedido (por exemplo, vagas ou um email) são ignorados."""
        self.guardar(descricao=DESCRICAO_NOVA, vagas="999", email=VALID_EMAIL)
        with self.app.app_context():
            curso = catalogo.por_chave(self.app.config, CURSO.chave)
        self.assertEqual(curso.vagas, CURSO.vagas)
