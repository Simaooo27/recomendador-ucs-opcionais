"""Em que ponto do percurso está cada utilizador (padrão State, versão simples).

Ver docs/geral/03-arquitetura-e-padroes.md, secção 4.6: o utilizador está num estado e
o estado decide o que a página inicial mostra. Começa por uma função; só se as regras
crescerem (US29, US31) vale a pena ter uma classe por estado.

Enquanto o questionário (US29) e a escolha de curso (US31) não existem, todas as contas
ativas estão no estado «sem curso»: conta criada, a seguir o questionário.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import texts


class EstadoPercurso(str, Enum):
    SEM_CURSO = "sem_curso"                  # conta criada; a seguir, o questionário
    A_ESCOLHER_CURSO = "a_escolher_curso"    # respondeu ao questionário (US29)
    COM_CURSO = "com_curso"                  # escolheu o curso (US31); a seguir, as opcionais


# Índice do passo atual (em texts.HOME_PATH_STEPS) em cada estado.
_PASSO_ATUAL = {
    EstadoPercurso.SEM_CURSO: 1,
    EstadoPercurso.A_ESCOLHER_CURSO: 2,
    EstadoPercurso.COM_CURSO: 3,
}


@dataclass(frozen=True)
class Passo:
    titulo: str
    texto: str
    situacao: str  # "feito", "atual" ou "depois" (usado no CSS e nos testes)


def estado_do_utilizador(user) -> EstadoPercurso:
    """Estado do percurso de um aluno. Até à US29/US31, todos estão «sem curso»."""
    return EstadoPercurso.SEM_CURSO


def passos(estado: EstadoPercurso) -> list[Passo]:
    """Os passos da linha do tempo, marcados como feitos, atual ou para depois."""
    atual = _PASSO_ATUAL[estado]
    resultado = []
    for indice, passo in enumerate(texts.HOME_PATH_STEPS):
        situacao = "feito" if indice < atual else "atual" if indice == atual else "depois"
        resultado.append(Passo(passo["titulo"], passo["texto"], situacao))
    return resultado
