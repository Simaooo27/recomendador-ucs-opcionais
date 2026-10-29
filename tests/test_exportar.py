"""US46: exportar os meus dados (direito de acesso e de portabilidade)."""
from __future__ import annotations

import json
import sqlite3

from app import texts
from app.catalogo import repository as catalogo_repository
from app.config import default_config
from tests.base import CSRF_TOKEN, VALID_EMAIL, VALID_NOME, VALID_PASSWORD, AppTestCase

CURSO = catalogo_repository.todos(default_config()["CATALOGO_CSV"])[0]
OUTRO_EMAIL = "outra@gmail.com"


class ExportarTestCase(AppTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.create_active_user()
        self.login()
        self.user_id = self.fetch_user()["id"]

    def _exportar(self, password=VALID_PASSWORD, *, with_csrf=True, client=None):
        client = client or self.client
        if with_csrf:
            self.set_csrf(client)
        dados = {"csrf_token": CSRF_TOKEN} if with_csrf else {}
        if password is not None:
            dados["password"] = password
        return client.post("/auth/conta/exportar", data=dados)

    def _sql(self, consulta: str, parametros: tuple) -> None:
        ligacao = sqlite3.connect(self.db_path)
        try:
            ligacao.execute(consulta, parametros)
            ligacao.commit()
        finally:
            ligacao.close()

    def _criar_dados(self, user_id: int, *, media: float = 15.2, curso: str = CURSO.curso) -> None:
        """Uma decisão, um plano partilhado, uma conversa e pedidos ao LLM, como os de um aluno real."""
        self._sql(
            "INSERT INTO decisoes (user_id, curso_chave, curso, instituicao, origem, sugeridos, decidida_em) "
            "VALUES (?, ?, ?, ?, 'catalogo', '[]', '2026-10-20T10:00:00+00:00')",
            (user_id, CURSO.chave, curso, CURSO.instituicao),
        )
        self._sql(
            "INSERT INTO planos_candidatura (user_id, media, exames, opcoes, partilha, atualizado_em) "
            "VALUES (?, ?, '{\"18\": 140.0}', ?, ?, '2026-10-21T10:00:00+00:00')",
            (user_id, media, json.dumps([CURSO.chave, "9999-0000"]), f"codigo-secreto-{user_id}"),
        )
        self._sql(
            "INSERT INTO conversas_orientacao (user_id, mensagens, sugestao, atualizada_em) "
            "VALUES (?, '[{\"papel\": \"utilizador\", \"texto\": \"gosto de livros\"}]', NULL, '2026-10-22T10:00:00+00:00')",
            (user_id,),
        )
        self._sql("INSERT INTO pedidos_llm (user_id, dia, total) VALUES (?, '2026-10-01', 3)", (user_id,))


class PaginaTests(ExportarTestCase):
    def test_a_minha_conta_tem_a_ligacao(self):
        html = self.client.get("/auth/conta").get_data(as_text=True)
        self.assertIn('href="/auth/conta/exportar"', html)
        self.assertIn(texts.CONTA_EXPORTAR_LIGACAO, html)

    def test_a_pagina_diz_o_que_vai_no_ficheiro_e_pede_a_palavra_passe(self):
        html = self.client.get("/auth/conta/exportar").get_data(as_text=True)
        for item in texts.EXPORTAR_ITENS:
            self.assertIn(item, html)
        self.assertIn('type="password"', html)
        self.assertIn('name="csrf_token"', html)

    def test_sem_sessao_vai_para_o_inicio_de_sessao(self):
        anonimo = self.app.test_client()
        for pedido in (anonimo.get, anonimo.post):
            with self.subTest(metodo=pedido.__name__):
                response = pedido("/auth/conta/exportar")
                self.assertIn(response.status_code, (302, 400))   # o POST sem CSRF é recusado antes
        self.assertTrue(anonimo.get("/auth/conta/exportar").headers["Location"].endswith("/auth/entrar"))


class PalavraPasseTests(ExportarTestCase):
    """Critério: pede a palavra-passe antes de descarregar."""

    def test_palavra_passe_errada_nao_descarrega(self):
        response = self._exportar("palavra-errada-123")
        self.assertEqual(response.status_code, 422)
        self.assertIn(texts.EXPORTAR_ERRO_PASSWORD, response.get_data(as_text=True))
        self.assertNotIn("attachment", response.headers.get("Content-Disposition", ""))

    def test_sem_palavra_passe_nao_descarrega(self):
        self.assertEqual(self._exportar(None).status_code, 422)

    def test_sem_csrf_e_recusado(self):
        self.assertEqual(self._exportar(with_csrf=False).status_code, 400)


class FicheiroTests(ExportarTestCase):
    """Critério: ficheiro JSON com a conta (sem a palavra-passe), as decisões, as notas e o plano."""

    def _ficheiro(self) -> dict:
        response = self._exportar()
        self.assertEqual(response.status_code, 200)
        return json.loads(response.get_data(as_text=True))

    def test_e_um_ficheiro_json_para_descarregar_e_sem_cache(self):
        response = self._exportar()
        self.assertEqual(response.mimetype, "application/json")
        self.assertRegex(response.headers["Content-Disposition"], r'attachment; filename="optabem-os-meus-dados-\d{4}-\d{2}-\d{2}\.json"')
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_tem_a_conta_sem_a_palavra_passe(self):
        ficheiro = self._ficheiro()
        self.assertEqual(ficheiro["conta"]["email"], VALID_EMAIL)
        self.assertEqual(ficheiro["conta"]["nome"], VALID_NOME)
        self.assertIsNotNone(ficheiro["conta"]["confirmada_em"])
        texto = json.dumps(ficheiro)
        self.assertNotIn(VALID_PASSWORD, texto)
        self.assertNotIn(self.fetch_user()["password_hash"], texto)
        self.assertNotIn(self.fetch_user()["confirmation_nonce"], texto)

    def test_sem_dados_ainda_o_ficheiro_tem_as_secoes_vazias(self):
        ficheiro = self._ficheiro()
        self.assertEqual(ficheiro["decisoes_do_percurso"], [])
        self.assertIsNone(ficheiro["plano_de_candidatura"])
        self.assertIsNone(ficheiro["conversa_de_orientacao"])
        self.assertEqual(ficheiro["pedidos_ao_assistente_por_dia"], [])

    def test_tem_as_decisoes_as_notas_o_plano_e_a_conversa(self):
        self._criar_dados(self.user_id)
        ficheiro = self._ficheiro()
        self.assertEqual([d["curso_chave"] for d in ficheiro["decisoes_do_percurso"]], [CURSO.chave])
        plano = ficheiro["plano_de_candidatura"]
        self.assertEqual(plano["media_do_secundario"], 15.2)
        self.assertEqual(plano["exames"], {"18": 140.0})
        self.assertEqual(plano["opcoes"][0], {"posicao": 1, "curso_chave": CURSO.chave, "curso": CURSO.curso, "instituicao": CURSO.instituicao})
        self.assertTrue(plano["partilhado"])
        self.assertEqual(ficheiro["conversa_de_orientacao"]["mensagens"][0]["texto"], "gosto de livros")
        self.assertEqual(ficheiro["pedidos_ao_assistente_por_dia"], [{"dia": "2026-10-01", "total": 3}])

    def test_um_curso_que_saiu_do_catalogo_fica_na_lista_sem_nome(self):
        self._criar_dados(self.user_id)
        opcao = self._ficheiro()["plano_de_candidatura"]["opcoes"][1]
        self.assertEqual(opcao, {"posicao": 2, "curso_chave": "9999-0000", "curso": None, "instituicao": None})

    def test_o_codigo_da_ligacao_de_partilha_nao_vai_no_ficheiro(self):
        """Quem tem o código vê o plano: o ficheiro diz só que está partilhado."""
        self._criar_dados(self.user_id)
        self.assertNotIn(f"codigo-secreto-{self.user_id}", json.dumps(self._ficheiro()))

    def test_as_decisoes_vao_da_mais_antiga_para_a_mais_recente(self):
        self._criar_dados(self.user_id)
        self._sql(
            "INSERT INTO decisoes (user_id, curso_chave, curso, instituicao, origem, sugeridos, decidida_em) "
            "VALUES (?, 'outra', 'Curso mais recente', 'X', 'catalogo', '[]', '2026-10-25T10:00:00+00:00')",
            (self.user_id,),
        )
        cursos = [d["curso"] for d in self._ficheiro()["decisoes_do_percurso"]]
        self.assertEqual(cursos, [CURSO.curso, "Curso mais recente"])


class OutrosUtilizadoresTests(ExportarTestCase):
    """Critério: nunca inclui dados de outros utilizadores."""

    def test_so_tem_os_dados_de_quem_descarrega(self):
        self.create_active_user(email=OUTRO_EMAIL)
        outro_id = self.fetch_user(OUTRO_EMAIL)["id"]
        self._criar_dados(outro_id, media=11.1, curso="Curso do outro aluno")
        ficheiro = json.dumps(self._exportar().get_json())
        self.assertNotIn(OUTRO_EMAIL, ficheiro)
        self.assertNotIn("11.1", ficheiro)
        self.assertNotIn("Curso do outro aluno", ficheiro)
        self.assertNotIn("gosto de livros", ficheiro)

    def test_a_palavra_passe_de_outra_conta_nao_serve(self):
        self.create_active_user(email=OUTRO_EMAIL, password="outra-palavra-9")
        self.assertEqual(self._exportar("outra-palavra-9").status_code, 422)


class PoliticaDePrivacidadeTests(AppTestCase):
    def test_a_politica_explica_como_descarregar_os_dados(self):
        html = self.client.get("/privacidade").get_data(as_text=True)
        self.assertIn("Descarregar os meus dados", html)
        self.assertIn("portabilidade", html)
