"""Em que ponto do percurso está cada utilizador (padrão State, versão simples).

Ver docs/geral/03-arquitetura-e-padroes.md, secção 4.6: o utilizador está num estado e
o estado decide o que a página inicial mostra. Começa por uma função; só se as regras
crescerem (US29, US31) vale a pena ter uma classe por estado.

Com a conversa de orientação (US29), quem já recebeu sugestões passa a «a escolher curso».
Enquanto a escolha de curso (US31) não existe, ninguém chega a «com curso».
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import texts


class EstadoPercurso(str, Enum):
    SEM_CURSO = "sem_curso"                  # conta criada; a seguir, a conversa de orientação
    A_ESCOLHER_CURSO = "a_escolher_curso"    # a conversa terminou com sugestões (US29)
    COM_CURSO = "com_curso"                  # escolheu o curso (US31); a seguir, as opcionais


# Índice do passo atual (em texts.HOME_PATH_STEPS) em cada estado.
_PASSO_ATUAL = {
    EstadoPercurso.SEM_CURSO: 1,
    EstadoPercurso.A_ESCOLHER_CURSO: 2,
    EstadoPercurso.COM_CURSO: 3,
}


# O que o passo atual oferece em cada estado: (texto do botão, página). Sem entrada = «em breve».
_ACAO = {
    EstadoPercurso.SEM_CURSO: (texts.HOME_ACTION_CONVERSA, "orientacao.pagina"),
    EstadoPercurso.A_ESCOLHER_CURSO: (texts.HOME_ACTION_CONTINUAR, "orientacao.pagina"),
}


@dataclass(frozen=True)
class Passo:
    titulo: str
    texto: str
    situacao: str  # "feito", "atual" ou "depois" (usado no CSS e nos testes)
    acao: tuple[str, str] | None = None   # (texto do botão, página) no passo atual


def estado_do_utilizador(user, *, conversa_terminada: bool = False) -> EstadoPercurso:
    """Estado do percurso de um aluno. A escolha de curso (US31) ainda não existe."""
    return EstadoPercurso.A_ESCOLHER_CURSO if conversa_terminada else EstadoPercurso.SEM_CURSO


def passos(estado: EstadoPercurso) -> list[Passo]:
    """Os passos da linha do tempo, marcados como feitos, atual ou para depois."""
    atual = _PASSO_ATUAL[estado]
    resultado = []
    for indice, passo in enumerate(texts.HOME_PATH_STEPS):
        situacao = "feito" if indice < atual else "atual" if indice == atual else "depois"
        acao = _ACAO.get(estado) if situacao == "atual" else None
        resultado.append(Passo(passo["titulo"], passo["texto"], situacao, acao))
    return resultado
