"""Conversa de orientação conduzida pelo LLM (spike da US29 e da US30), com o LLMFalso (sem rede)."""
from __future__ import annotations

import json
import unittest

from app.catalogo import repository
from app.config import default_config
from app.llm import Mensagem, RespostaInvalida
from app.llm.adaptadores import LLMFalso
from app.llm.decoradores import EMAIL_REMOVIDO, ProtegerDadosPessoais
from app.orientacao import conversa
from tests.base import AppTestCase

CATALOGO = repository.todos(default_config()["CATALOGO_CSV"])


def sugestao(*ids: str, texto: str = "Estes cursos combinam consigo.") -> str:
    return json.dumps({"tipo": "sugestao", "texto": texto, "cursos": [{"id": i, "explicacao": f"porque {i}"} for i in ids]})


class CatalogoNasInstrucoesTests(unittest.TestCase):
    def test_o_catalogo_tem_cursos(self):
        self.assertGreaterEqual(len(CATALOGO), 2)

    def test_cada_curso_vai_com_o_identificador_instituicao_curso(self):
        texto = conversa.instrucoes(CATALOGO)
        for curso in CATALOGO:
            self.assertIn(curso.chave + " | " + curso.curso, texto)
        self.assertNotIn("$catalogo", texto)
        self.assertNotIn("$max_perguntas", texto)

    def test_o_mesmo_codigo_de_curso_em_varias_instituicoes_e_distinguido(self):
        # O código DGES de um curso repete-se entre instituições: só o par instituição-curso é único.
        chaves = [c.chave for c in CATALOGO]
        self.assertEqual(len(chaves), len(set(chaves)))


class InterpretarTests(unittest.TestCase):
    def test_aceita_json_simples_e_dentro_de_bloco(self):
        self.assertEqual(conversa.interpretar('{"tipo": "pergunta", "texto": "?"}')["tipo"], "pergunta")
        self.assertEqual(conversa.interpretar('```json\n{"tipo": "pergunta", "texto": "?"}\n```')["texto"], "?")

    def test_recusa_o_que_nao_segue_o_formato(self):
        for texto in ("Olá! Que curso quer?", "[1, 2]", '{"tipo": "outra"}'):
            with self.subTest(texto=texto), self.assertRaises(RespostaInvalida):
                conversa.interpretar(texto)


class ValidarContraCatalogoTests(unittest.TestCase):
    """RN09: só se mostram cursos que existem no catálogo."""

    def test_aceita_cursos_do_catalogo(self):
        a, b = CATALOGO[0].chave, CATALOGO[1].chave
        resultado = conversa.validar_contra_catalogo(json.loads(sugestao(a, b)), CATALOGO)
        self.assertEqual([s.curso.chave for s in resultado.cursos], [a, b])
        self.assertEqual(resultado.cursos[0].explicacao, f"porque {a}")
        self.assertEqual(resultado.descartados, ())

    def test_descarta_cursos_inventados(self):
        a = CATALOGO[0].chave
        resultado = conversa.validar_contra_catalogo(json.loads(sugestao("9999-0000", a, "Medicina em Harvard")), CATALOGO)
        self.assertEqual([s.curso.chave for s in resultado.cursos], [a])
        self.assertEqual(resultado.descartados, ("9999-0000", "Medicina em Harvard"))

    def test_so_o_codigo_do_curso_sem_instituicao_nao_chega(self):
        resultado = conversa.validar_contra_catalogo(json.loads(sugestao(CATALOGO[0].codigo_curso)), CATALOGO)
        self.assertEqual(resultado.cursos, ())

    def test_sem_repetidos_e_no_maximo_tres(self):
        chaves = [c.chave for c in CATALOGO[:5]]
        resultado = conversa.validar_contra_catalogo(json.loads(sugestao(chaves[0], chaves[0], *chaves[1:])), CATALOGO)
        self.assertEqual([s.curso.chave for s in resultado.cursos], chaves[:3])

    def test_nenhum_curso_valido_devolve_lista_vazia(self):
        resultado = conversa.validar_contra_catalogo({"tipo": "sugestao", "texto": "x", "cursos": "nada"}, CATALOGO)
        self.assertEqual(resultado.cursos, ())


class ProximoPassoTests(unittest.TestCase):
    def test_comeca_com_a_abertura_e_devolve_a_pergunta(self):
        falso = LLMFalso(['{"tipo": "pergunta", "texto": "Que  disciplinas\\n prefere?"}'])
        passo = conversa.proximo_passo(falso, CATALOGO, [])
        self.assertEqual(passo, conversa.Pergunta("Que disciplinas prefere?"))
        instrucoes, mensagens = falso.pedidos[0]
        self.assertEqual(mensagens, (Mensagem("utilizador", conversa.ABERTURA),))
        self.assertNotIn(conversa.PEDIDO_DE_SUGESTAO, instrucoes)

    def test_sugestao_validada(self):
        falso = LLMFalso([sugestao(CATALOGO[0].chave, "inventado")])
        passo = conversa.proximo_passo(falso, CATALOGO, [Mensagem("assistente", "?"), Mensagem("utilizador", "gosto de dados")])
        self.assertIsInstance(passo, conversa.Sugestao)
        self.assertEqual(len(passo.cursos), 1)
        self.assertEqual(passo.descartados, ("inventado",))

    def test_depois_do_limite_de_perguntas_pede_a_sugestao(self):
        historico = []
        for i in range(conversa.LIMITE_PERGUNTAS):
            historico += [Mensagem("assistente", f"pergunta {i}"), Mensagem("utilizador", f"resposta {i}")]
        falso = LLMFalso([sugestao(CATALOGO[0].chave)])
        conversa.proximo_passo(falso, CATALOGO, historico)
        self.assertTrue(falso.pedidos[0][0].endswith(conversa.PEDIDO_DE_SUGESTAO))

    def test_depois_do_limite_uma_pergunta_e_resposta_invalida(self):
        historico = []
        for i in range(conversa.LIMITE_PERGUNTAS):
            historico += [Mensagem("assistente", f"pergunta {i}"), Mensagem("utilizador", f"resposta {i}")]
        with self.assertRaises(RespostaInvalida):
            conversa.proximo_passo(LLMFalso(['{"tipo": "pergunta", "texto": "mais uma?"}']), CATALOGO, historico)

    def test_pedir_a_sugestao_antes_do_limite_tambem_nao_aceita_perguntas(self):
        with self.assertRaises(RespostaInvalida):
            conversa.proximo_passo(
                LLMFalso(['{"tipo": "pergunta", "texto": "mais uma?"}']), CATALOGO, [], forcar_sugestao=True
            )

    def test_o_llm_falso_sem_respostas_simula_uma_conversa_curta(self):
        falso = LLMFalso()
        self.assertIsInstance(conversa.proximo_passo(falso, CATALOGO, []), conversa.Pergunta)
        historico = [Mensagem("assistente", "?"), Mensagem("utilizador", "gosto de dados")]
        self.assertIsInstance(conversa.proximo_passo(falso, CATALOGO, historico), conversa.Sugestao)

    def test_respostas_longas_sao_cortadas(self):
        falso = LLMFalso()
        conversa.proximo_passo(falso, CATALOGO, [Mensagem("assistente", "?"), Mensagem("utilizador", "a" * 5000)])
        self.assertEqual(len(falso.pedidos[0][1][-1].texto), conversa.MAX_CARACTERES_RESPOSTA)

    def test_nao_envia_dados_pessoais_escritos_pelo_utilizador(self):
        falso = LLMFalso()
        conversa.proximo_passo(
            ProtegerDadosPessoais(falso), CATALOGO, [Mensagem("assistente", "?"), Mensagem("utilizador", "sou a ana@gmail.com")]
        )
        enviado = json.dumps([m.texto for m in falso.pedidos[0][1]])
        self.assertNotIn("ana@gmail.com", enviado)
        self.assertIn(EMAIL_REMOVIDO, enviado)

    def test_resposta_fora_do_formato(self):
        with self.assertRaises(RespostaInvalida):
            conversa.proximo_passo(LLMFalso(["Claro! Sugiro Medicina."]), CATALOGO, [])


class ComandoLlmTesteTests(AppTestCase):
    """O comando que o PO corre com a chave real; aqui com o LLM falso."""

    def test_corre_com_o_llm_falso(self):
        resultado = self.app.test_cli_runner().invoke(args=["llm-teste", "--backend", "falso"])
        self.assertEqual(resultado.exit_code, 0, resultado.output)
        self.assertIn("LLM: falso", resultado.output)
        self.assertIn("1.º pedido", resultado.output)
        self.assertIn("2.º pedido", resultado.output)

    def test_sem_chave_explica_o_que_falta_sem_rebentar(self):
        resultado = self.app.test_cli_runner().invoke(args=["llm-teste", "--backend", "gemini"])
        self.assertEqual(resultado.exit_code, 1)
        self.assertIn("GEMINI_API_KEY", resultado.output)

    def test_backend_desconhecido(self):
        resultado = self.app.test_cli_runner().invoke(args=["llm-teste", "--backend", "xpto"])
        self.assertEqual(resultado.exit_code, 1)
        self.assertIn("LLM_BACKEND desconhecido", resultado.output)


if __name__ == "__main__":
    unittest.main()
