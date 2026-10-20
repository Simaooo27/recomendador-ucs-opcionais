"""Ligação ao LLM (spike da US30): interface, adaptadores, fábrica e proteção de dados (RNF12).

Nenhum teste usa a rede: os adaptadores recebem um transporte falso que guarda o pedido.
"""
from __future__ import annotations

import json
import unittest

from app.llm import (
    LimiteAtingido,
    LLMIndisponivel,
    Mensagem,
    RespostaInvalida,
    criar_cliente_llm,
)
from app.llm.adaptadores import AdaptadorGemini, AdaptadorGroq, AdaptadorOllama, ErroHTTP, LLMFalso
from app.llm.decoradores import EMAIL_REMOVIDO, NUMERO_REMOVIDO, ProtegerDadosPessoais, remover_dados_pessoais

CHAVE = "chave-secreta-de-teste-123"
CONVERSA = [
    Mensagem("utilizador", "Olá"),
    Mensagem("assistente", "Que disciplinas prefere?"),
    Mensagem("utilizador", "Informática"),
]


class TransporteFalso:
    def __init__(self, resposta: dict | None = None, erro: Exception | None = None) -> None:
        self.resposta, self.erro, self.pedidos = resposta, erro, []

    def __call__(self, url, cabecalhos, corpo, timeout):
        self.pedidos.append({"url": url, "cabecalhos": cabecalhos, "corpo": corpo, "timeout": timeout})
        if self.erro:
            raise self.erro
        return self.resposta


def resposta_gemini(texto: str) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": texto}]}, "finishReason": "STOP"}]}


def resposta_groq(texto: str) -> dict:
    return {"choices": [{"message": {"role": "assistant", "content": texto}}]}


def resposta_ollama(texto: str) -> dict:
    return {"model": "qwen3:4b", "message": {"role": "assistant", "content": texto}, "done": True}


class FabricaTests(unittest.TestCase):
    def test_por_omissao_usa_o_falso_sem_rede(self):
        cliente = criar_cliente_llm({})
        self.assertEqual(cliente.nome, "falso")
        self.assertTrue(cliente.conversar("regras", CONVERSA))

    def test_escolhe_o_gemini_com_o_modelo_por_omissao(self):
        cliente = criar_cliente_llm({"LLM_BACKEND": "gemini", "GEMINI_API_KEY": CHAVE})
        self.assertEqual(cliente.nome, "gemini/gemini-3.5-flash-lite")

    def test_escolhe_o_groq_e_aceita_outro_modelo(self):
        cliente = criar_cliente_llm({"LLM_BACKEND": "Groq", "GROQ_API_KEY": CHAVE, "LLM_MODELO": "openai/gpt-oss-20b"})
        self.assertEqual(cliente.nome, "groq/openai/gpt-oss-20b")

    def test_sem_chave_da_erro_claro(self):
        with self.assertRaisesRegex(LLMIndisponivel, "GEMINI_API_KEY"):
            criar_cliente_llm({"LLM_BACKEND": "gemini", "GEMINI_API_KEY": ""})
        with self.assertRaisesRegex(LLMIndisponivel, "GROQ_API_KEY"):
            criar_cliente_llm({"LLM_BACKEND": "groq"})

    def test_backend_desconhecido(self):
        with self.assertRaisesRegex(RuntimeError, "LLM_BACKEND desconhecido"):
            criar_cliente_llm({"LLM_BACKEND": "openai"})

    def test_escolhe_o_ollama_com_o_qwen3_por_omissao(self):
        cliente = criar_cliente_llm({"LLM_BACKEND": "ollama", "OLLAMA_BASE_URL": "https://servidor.exemplo", "OLLAMA_API_KEY": CHAVE})
        self.assertEqual(cliente.nome, "ollama/qwen3:4b")

    def test_ollama_sem_endereco_da_erro_claro(self):
        with self.assertRaisesRegex(LLMIndisponivel, "OLLAMA_BASE_URL"):
            criar_cliente_llm({"LLM_BACKEND": "ollama", "OLLAMA_API_KEY": CHAVE})

    def test_o_cliente_vem_sempre_protegido(self):
        for config in (
            {},
            {"LLM_BACKEND": "gemini", "GEMINI_API_KEY": CHAVE},
            {"LLM_BACKEND": "groq", "GROQ_API_KEY": CHAVE},
            {"LLM_BACKEND": "ollama", "OLLAMA_BASE_URL": "https://servidor.exemplo"},
        ):
            self.assertIsInstance(criar_cliente_llm(config), ProtegerDadosPessoais)


class LLMFalsoTests(unittest.TestCase):
    def test_devolve_as_respostas_por_ordem_e_repete_a_ultima(self):
        falso = LLMFalso(["a", "b"])
        self.assertEqual([falso.conversar("x", CONVERSA) for _ in range(3)], ["a", "b", "b"])
        self.assertEqual(len(falso.pedidos), 3)


class AdaptadorGeminiTests(unittest.TestCase):
    def setUp(self):
        self.transporte = TransporteFalso(resposta_gemini('{"tipo": "pergunta", "texto": "?"}'))
        self.gemini = AdaptadorGemini(chave=CHAVE, modelo="gemini-x", transporte=self.transporte)

    def test_monta_o_pedido_no_formato_do_gemini(self):
        self.assertEqual(self.gemini.conversar("regras fixas", CONVERSA), '{"tipo": "pergunta", "texto": "?"}')
        pedido = self.transporte.pedidos[0]
        self.assertTrue(pedido["url"].endswith("/models/gemini-x:generateContent"))
        corpo = pedido["corpo"]
        self.assertEqual(corpo["systemInstruction"]["parts"][0]["text"], "regras fixas")
        self.assertEqual([c["role"] for c in corpo["contents"]], ["user", "model", "user"])
        self.assertEqual(corpo["contents"][2]["parts"][0]["text"], "Informática")
        self.assertEqual(corpo["generationConfig"]["responseMimeType"], "application/json")

    def test_a_chave_vai_no_cabecalho_e_nunca_no_endereco(self):
        self.gemini.conversar("r", CONVERSA)
        pedido = self.transporte.pedidos[0]
        self.assertEqual(pedido["cabecalhos"], {"x-goog-api-key": CHAVE})
        self.assertNotIn(CHAVE, pedido["url"])
        self.assertNotIn(CHAVE, json.dumps(pedido["corpo"]))

    def test_ignora_as_partes_de_raciocinio(self):
        self.transporte.resposta = {
            "candidates": [{"content": {"parts": [{"text": "a pensar", "thought": True}, {"text": "{}"}]}}]
        }
        self.assertEqual(self.gemini.conversar("r", CONVERSA), "{}")

    def test_pedido_bloqueado_ou_vazio(self):
        self.transporte.resposta = {"promptFeedback": {"blockReason": "SAFETY"}}
        with self.assertRaisesRegex(RespostaInvalida, "SAFETY"):
            self.gemini.conversar("r", CONVERSA)
        self.transporte.resposta = resposta_gemini("  ")
        with self.assertRaises(RespostaInvalida):
            self.gemini.conversar("r", CONVERSA)

    def test_limite_atingido(self):
        corpo = json.dumps({"error": {"code": 429, "message": "Quota exceeded", "status": "RESOURCE_EXHAUSTED"}})
        self.transporte.erro = ErroHTTP(429, corpo)
        with self.assertRaisesRegex(LimiteAtingido, "Quota exceeded"):
            self.gemini.conversar("r", CONVERSA)

    def test_erros_nunca_mostram_a_chave(self):
        for codigo in (400, 401, 403, 404, 429, 500):
            self.transporte.erro = ErroHTTP(codigo, json.dumps({"error": {"message": f"key {CHAVE} invalid"}}))
            with self.assertRaises((LimiteAtingido, LLMIndisponivel)) as contexto:
                self.gemini.conversar("r", CONVERSA)
            self.assertNotIn(CHAVE, str(contexto.exception))

    def test_modelo_inexistente(self):
        self.transporte.erro = ErroHTTP(404, "não é json")
        with self.assertRaisesRegex(LLMIndisponivel, "gemini-x"):
            self.gemini.conversar("r", CONVERSA)


class AdaptadorGroqTests(unittest.TestCase):
    def setUp(self):
        self.transporte = TransporteFalso(resposta_groq('{"tipo": "pergunta", "texto": "?"}'))
        self.groq = AdaptadorGroq(chave=CHAVE, modelo="openai/gpt-oss-120b", transporte=self.transporte)

    def test_monta_o_pedido_no_formato_openai(self):
        self.assertEqual(self.groq.conversar("regras fixas", CONVERSA), '{"tipo": "pergunta", "texto": "?"}')
        pedido = self.transporte.pedidos[0]
        self.assertEqual(pedido["cabecalhos"], {"Authorization": f"Bearer {CHAVE}"})
        mensagens = pedido["corpo"]["messages"]
        self.assertEqual([m["role"] for m in mensagens], ["system", "user", "assistant", "user"])
        self.assertEqual(mensagens[0]["content"], "regras fixas")
        self.assertEqual(pedido["corpo"]["response_format"], {"type": "json_object"})

    def test_resposta_sem_choices(self):
        self.transporte.resposta = {"erro": "?"}
        with self.assertRaises(RespostaInvalida):
            self.groq.conversar("r", CONVERSA)

    def test_limite_atingido(self):
        self.transporte.erro = ErroHTTP(429, json.dumps({"error": {"message": "Rate limit reached"}}))
        with self.assertRaisesRegex(LimiteAtingido, "Rate limit"):
            self.groq.conversar("r", CONVERSA)


class AdaptadorOllamaTests(unittest.TestCase):
    def setUp(self):
        self.transporte = TransporteFalso(resposta_ollama('{"tipo": "pergunta", "texto": "?"}'))
        self.ollama = AdaptadorOllama(
            endereco="https://servidor.exemplo:443/", chave=CHAVE, modelo="qwen3:4b", transporte=self.transporte
        )

    def test_monta_o_pedido_no_formato_do_ollama(self):
        self.assertEqual(self.ollama.conversar("regras", CONVERSA), '{"tipo": "pergunta", "texto": "?"}')
        pedido = self.transporte.pedidos[0]
        self.assertEqual(pedido["url"], "https://servidor.exemplo:443/api/chat")
        corpo = pedido["corpo"]
        self.assertEqual(corpo["model"], "qwen3:4b")
        self.assertEqual(corpo["messages"][0], {"role": "system", "content": "regras"})
        self.assertEqual([m["role"] for m in corpo["messages"][1:]], ["user", "assistant", "user"])
        self.assertEqual(corpo["format"], "json")
        self.assertFalse(corpo["stream"])
        self.assertFalse(corpo["think"])
        # As instruções com o catálogo têm cerca de 3700 tokens: a janela tem de chegar.
        self.assertGreaterEqual(corpo["options"]["num_ctx"], 8192)

    def test_o_token_vai_no_cabecalho_e_nunca_no_endereco(self):
        self.ollama.conversar("regras", CONVERSA)
        pedido = self.transporte.pedidos[0]
        self.assertEqual(pedido["cabecalhos"], {"Authorization": f"Bearer {CHAVE}"})
        self.assertNotIn(CHAVE, pedido["url"])

    def test_o_token_nunca_vai_por_http(self):
        with self.assertRaisesRegex(LLMIndisponivel, "https"):
            AdaptadorOllama(endereco="http://servidor.exemplo", chave=CHAVE, modelo="qwen3:4b")

    def test_servidor_local_sem_token_pode_ser_http(self):
        transporte = TransporteFalso(resposta_ollama('{"tipo": "pergunta", "texto": "?"}'))
        local = AdaptadorOllama(endereco="http://localhost:11434", chave="", modelo="qwen3:4b", transporte=transporte)
        local.conversar("regras", CONVERSA)
        self.assertEqual(transporte.pedidos[0]["cabecalhos"], {})

    def test_ignora_o_bloco_de_raciocinio(self):
        self.transporte.resposta = resposta_ollama('<think>a pensar…</think>\n{"tipo": "pergunta", "texto": "?"}')
        self.assertEqual(self.ollama.conversar("regras", CONVERSA), '{"tipo": "pergunta", "texto": "?"}')

    def test_resposta_vazia(self):
        self.transporte.resposta = resposta_ollama("   ")
        with self.assertRaises(RespostaInvalida):
            self.ollama.conversar("regras", CONVERSA)

    def test_erros_nunca_mostram_o_token(self):
        self.transporte.erro = ErroHTTP(401, f'{{"error": "token {CHAVE} inválido"}}')
        with self.assertRaises(LLMIndisponivel) as contexto:
            self.ollama.conversar("regras", CONVERSA)
        self.assertNotIn(CHAVE, str(contexto.exception))

    def test_modelo_inexistente(self):
        self.transporte.erro = ErroHTTP(404, '{"error": "model \\"qwen9\\" not found"}')
        with self.assertRaisesRegex(LLMIndisponivel, "não existe"):
            self.ollama.conversar("regras", CONVERSA)

    def test_servidor_ocupado(self):
        self.transporte.erro = ErroHTTP(429, '{"error": "too many requests"}')
        with self.assertRaises(LimiteAtingido):
            self.ollama.conversar("regras", CONVERSA)


class DadosPessoaisTests(unittest.TestCase):
    """RNF12: o que o utilizador escreve não leva email, telefone nem números de identificação."""

    def test_apaga_emails(self):
        self.assertEqual(remover_dados_pessoais("escreva para ana.silva+x@gmail.com já"), f"escreva para {EMAIL_REMOVIDO} já")

    def test_apaga_telemoveis_e_numeros_de_identificacao(self):
        for texto in ("912345678", "912 345 678", "+351 912 345 678", "NIF 123456789", "4490-123", "PT50 0002 0123 1234 5678 9015 4"):
            with self.subTest(texto=texto):
                limpo = remover_dados_pessoais(texto)
                self.assertIn(NUMERO_REMOVIDO, limpo)
                self.assertFalse(any(ch.isdigit() for ch in limpo.replace("PT50", "")), limpo)

    def test_mantem_numeros_curtos_uteis(self):
        texto = "Tive 17 a Matemática, nota 138,3, em 2025, curso 9694, 3 anos."
        self.assertEqual(remover_dados_pessoais(texto), texto)

    def test_o_decorator_limpa_so_as_mensagens_do_utilizador(self):
        falso = LLMFalso(["ok"])
        protegido = ProtegerDadosPessoais(falso)
        protegido.conversar(
            "regras",
            [Mensagem("utilizador", "sou o rui@sapo.pt, 912345678"), Mensagem("assistente", "ajuda@optabem.pt")],
        )
        _, enviadas = falso.pedidos[0]
        self.assertEqual(enviadas[0].texto, f"sou o {EMAIL_REMOVIDO}, {NUMERO_REMOVIDO}")
        self.assertEqual(enviadas[1].texto, "ajuda@optabem.pt")


class SoOAdaptadorConheceOFornecedorTests(unittest.TestCase):
    """Secção 7 de docs/geral/03: nenhum ficheiro fora de app/llm/adaptadores.py fala com o fornecedor."""

    def test_enderecos_dos_fornecedores_so_em_adaptadores(self):
        from pathlib import Path

        raiz = Path(__file__).resolve().parent.parent / "app"
        for ficheiro in raiz.rglob("*.py"):
            if ficheiro.name == "adaptadores.py":
                continue
            texto = ficheiro.read_text(encoding="utf-8")
            for marca in ("googleapis.com", "api.groq.com", "google.genai", "import groq"):
                self.assertNotIn(marca, texto, f"{ficheiro.relative_to(raiz)} menciona {marca}")


if __name__ == "__main__":
    unittest.main()
