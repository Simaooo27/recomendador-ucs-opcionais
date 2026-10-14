"""Comportamentos à volta de qualquer ``ClienteLLM``, sem mexer nos adaptadores (padrão Decorator).

``ProtegerDadosPessoais`` (RNF12): a aplicação nunca envia ao LLM o email, o nome ou o
identificador da conta, porque a conversa de orientação não recebe a conta (ver orientacao/).
Mas numa conversa livre o próprio utilizador pode escrever esses dados. Este decorator apaga
emails e números longos (telemóvel, NIF, cartão de cidadão, IBAN) antes de cada envio.

Limite conhecido: não consegue reconhecer nomes próprios escritos no meio do texto. Por isso a
página da conversa (US29) avisa para não escrever dados pessoais, e as instruções dizem ao LLM
para não os pedir nem repetir.
"""
from __future__ import annotations

import re
from typing import Sequence

from .cliente import ClienteLLM, Mensagem

EMAIL_REMOVIDO = "[email removido]"
NUMERO_REMOVIDO = "[número removido]"

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
# IBAN português (PT50 seguido de 21 algarismos, com ou sem espaços).
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[0-9A-Z]{1,4}){4,8}\b")
# 7 ou mais algarismos seguidos, aceitando espaços, pontos ou hífenes entre grupos
# (telemóvel 912 345 678, +351 912345678, NIF 123456789, código postal 4490-123).
# Números curtos como uma nota (138,3), um ano (2025) ou um código de curso (9694) ficam.
_NUMERO_LONGO = re.compile(r"\+?\d(?:[ .-]?\d){6,}")


def remover_dados_pessoais(texto: str) -> str:
    texto = _EMAIL.sub(EMAIL_REMOVIDO, texto)
    texto = _IBAN.sub(NUMERO_REMOVIDO, texto)
    return _NUMERO_LONGO.sub(NUMERO_REMOVIDO, texto)


class ProtegerDadosPessoais:
    def __init__(self, cliente: ClienteLLM) -> None:
        self._cliente = cliente
        self.nome = cliente.nome

    def conversar(self, instrucoes: str, mensagens: Sequence[Mensagem]) -> str:
        limpas = [
            Mensagem(m.papel, remover_dados_pessoais(m.texto)) if m.papel == "utilizador" else m for m in mensagens
        ]
        return self._cliente.conversar(instrucoes, limpas)
