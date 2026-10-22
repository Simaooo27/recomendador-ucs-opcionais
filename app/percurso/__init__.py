"""O percurso de cada utilizador.

Este ficheiro decide em que ponto do percurso está cada utilizador (padrão State, versão
simples; ver docs/geral/03-arquitetura-e-padroes.md, secção 4.6): o estado decide o que a
página inicial mostra. As decisões (escolher curso, US31) estão em ``services.py``,
``repository.py`` e ``routes.py`` deste pacote.

- sem curso: conta criada; a seguir, a conversa de orientação (US29);
- a escolher curso: a conversa terminou com sugestões (US30);
- com curso: escolheu um curso (US31); o percurso desta release termina aqui (decisão dos PO, 22/10).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .. import texts


class EstadoPercurso(str, Enum):
    SEM_CURSO = "sem_curso"                  # conta criada; a seguir, a conversa de orientação
    A_ESCOLHER_CURSO = "a_escolher_curso"    # a conversa terminou com sugestões (US29)
    COM_CURSO = "com_curso"                  # escolheu o curso (US31); todos os passos ficam feitos


# Índice do passo atual (em texts.HOME_PATH_STEPS) em cada estado. «Com curso» aponta para depois
# do último passo: todos ficam «feito» (as opcionais saíram desta release, 22/10).
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

# Índice do passo «Escolher curso» em texts.HOME_PATH_STEPS: depois de escolher, mostra o curso.
_PASSO_CURSO = 2


@dataclass(frozen=True)
class Passo:
    titulo: str
    texto: str
    situacao: str  # "feito", "atual" ou "depois" (usado no CSS e nos testes)
    acao: tuple[str, str] | None = None   # (texto do botão, página) no passo atual


def estado_do_utilizador(user, *, conversa_terminada: bool = False, tem_curso: bool = False) -> EstadoPercurso:
    """Estado do percurso de um aluno. Quem já escolheu um curso fica «com curso», mesmo que volte a conversar."""
    if tem_curso:
        return EstadoPercurso.COM_CURSO
    return EstadoPercurso.A_ESCOLHER_CURSO if conversa_terminada else EstadoPercurso.SEM_CURSO


def passos(estado: EstadoPercurso, curso_escolhido=None) -> list[Passo]:
    """Os passos da linha do tempo, marcados como feitos, atual ou para depois.

    ``curso_escolhido`` (a decisão mais recente, US31) aparece no passo «Escolher curso», com a
    ligação para todas as decisões.
    """
    atual = _PASSO_ATUAL[estado]
    resultado = []
    for indice, passo in enumerate(texts.HOME_PATH_STEPS):
        situacao = "feito" if indice < atual else "atual" if indice == atual else "depois"
        acao = _ACAO.get(estado) if situacao == "atual" else None
        texto = passo["texto"]
        if indice == _PASSO_CURSO and curso_escolhido is not None:
            texto = texts.HOME_CURSO_ESCOLHIDO.format(curso=curso_escolhido.curso, instituicao=curso_escolhido.instituicao)
            acao = (texts.HOME_ACTION_VER_PERCURSO, "percurso.linha_tempo")
        resultado.append(Passo(passo["titulo"], texto, situacao, acao))
    return resultado
