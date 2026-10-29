"""Regras da conversa de orientação: começar, responder, tentar de novo e recomeçar (US29);
pedir as sugestões antes do fim, mostrá-las e continuar quando são poucas (US30).

A conversa fica guardada no servidor, uma por aluno. Estas funções nunca recebem nem enviam o
email ou o nome do aluno: só o identificador interno, usado para guardar a conversa (RNF12).
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping, Sequence

from .. import texts
from ..catalogo.repository import Curso
from ..llm import ClienteLLM, Mensagem
from ..llm.decoradores import remover_dados_pessoais
from . import conversa, notas, repository


class RespostaVazia(ValueError):
    pass


class RespostaLonga(ValueError):
    pass


@dataclass(frozen=True)
class EstadoConversa:
    mensagens: tuple[Mensagem, ...]
    sugestao: dict | None          # a sugestão final, em JSON (mostrada pela US30)
    usar_notas: bool = False       # US37: a pessoa autorizou o LLM a saber as provas feitas e a média aproximada

    @property
    def comecada(self) -> bool:
        return bool(self.mensagens)

    @property
    def terminada(self) -> bool:
        return self.sugestao is not None

    @property
    def a_espera_do_assistente(self) -> bool:
        """A última mensagem é do aluno: o LLM falhou e é preciso tentar de novo."""
        return self.comecada and not self.terminada and self.mensagens[-1].papel == "utilizador"

    @property
    def perguntas_feitas(self) -> int:
        return sum(1 for m in self.mensagens if m.papel == "assistente")

    @property
    def respostas_dadas(self) -> int:
        return sum(1 for m in self.mensagens if m.papel == "utilizador")

    @property
    def pode_pedir_sugestao(self) -> bool:
        """«Ver sugestões já»: depois de pelo menos uma resposta, enquanto a conversa decorre."""
        return self.comecada and not self.terminada and not self.a_espera_do_assistente and self.respostas_dadas > 0

    @property
    def sugestao_suficiente(self) -> bool:
        """A conversa terminou com pelo menos 2 cursos do catálogo (já validados ao guardar, RN09)."""
        return self.terminada and len(self.sugestao.get("cursos") or []) >= conversa.MIN_CURSOS_SUGERIDOS

    @property
    def sugestao_foi_pedida(self) -> bool:
        """A última mensagem é o pedido «Ver sugestões já» (para «Tentar de novo» voltar a pedi-las)."""
        return bool(self.mensagens) and self.mensagens[-1] == Mensagem("utilizador", texts.ORIENTACAO_PEDIDO_SUGESTAO)


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def obter(db: sqlite3.Connection, user_id: int) -> EstadoConversa:
    linha = repository.obter(db, user_id)
    if linha is None:
        return EstadoConversa((), None)
    mensagens = tuple(Mensagem(m["papel"], m["texto"]) for m in json.loads(linha["mensagens"]))
    return EstadoConversa(
        mensagens, json.loads(linha["sugestao"]) if linha["sugestao"] else None, bool(linha["usar_notas"])
    )


def _guardar(db: sqlite3.Connection, user_id: int, estado: EstadoConversa) -> None:
    mensagens = json.dumps([{"papel": m.papel, "texto": m.texto} for m in estado.mensagens], ensure_ascii=False)
    sugestao = json.dumps(estado.sugestao, ensure_ascii=False) if estado.sugestao is not None else None
    repository.guardar(db, user_id, mensagens, sugestao, _agora(), estado.usar_notas)


def _sugestao_em_json(sugestao: conversa.Sugestao) -> dict:
    return {
        "texto": sugestao.texto,
        "cursos": [{"id": s.curso.chave, "explicacao": s.explicacao} for s in sugestao.cursos],
        "descartados": list(sugestao.descartados),
    }


def _pedir_ao_llm(
    db: sqlite3.Connection,
    user_id: int,
    estado: EstadoConversa,
    cliente: ClienteLLM,
    catalogo: Sequence[Curso],
    *,
    forcar_sugestao: bool = False,
    nomes_das_provas: Mapping[str, str] | None = None,
) -> EstadoConversa:
    """Pede o próximo passo ao LLM e guarda-o. Se o LLM falhar, o erro sobe e a conversa fica como estava.

    Com autorização (US37), o LLM recebe as provas feitas e o intervalo da média, e o catálogo vai
    sem os cursos a que falta uma prova (``notas.py``). As notas lidas são as atuais do plano.
    """
    contexto = ""
    if estado.usar_notas:
        as_notas = _notas_do_plano(db, user_id)
        catalogo = notas.cursos_para_enviar(catalogo, as_notas)
        contexto = notas.contexto(as_notas, nomes_das_provas or {})
    passo = conversa.proximo_passo(cliente, catalogo, estado.mensagens, forcar_sugestao=forcar_sugestao, contexto=contexto)
    if isinstance(passo, conversa.Pergunta):
        novo = EstadoConversa(estado.mensagens + (Mensagem("assistente", passo.texto),), None, estado.usar_notas)
    else:
        texto = passo.texto or "Já tenho informação suficiente para lhe sugerir cursos."
        novo = EstadoConversa(
            estado.mensagens + (Mensagem("assistente", texto),), _sugestao_em_json(passo), estado.usar_notas
        )
    _guardar(db, user_id, novo)
    return novo


def _notas_do_plano(db: sqlite3.Connection, user_id: int):
    from ..candidatura import services as candidatura   # import local: o plano importa o percurso, que importa este módulo

    return candidatura.obter(db, user_id).notas


def pode_usar_notas(db: sqlite3.Connection, user_id: int) -> bool:
    """A pessoa já indicou exames no plano de candidatura: pode autorizar o assistente a usá-los (US37)."""
    return notas.tem_o_que_partilhar(_notas_do_plano(db, user_id))


def o_que_o_assistente_recebe(db: sqlite3.Connection, user_id: int, nomes_das_provas: Mapping[str, str]) -> tuple[list[str], tuple[int, int] | None]:
    """Para mostrar antes de autorizar: os nomes dos exames e o intervalo da média (nunca a exata)."""
    as_notas = _notas_do_plano(db, user_id)
    intervalo = notas.intervalo_da_media(as_notas.media) if as_notas.media is not None else None
    return notas.nomes_dos_exames(as_notas, nomes_das_provas), intervalo


def em_falta_nas_sugestoes(
    db: sqlite3.Connection,
    user_id: int,
    estado: EstadoConversa,
    sugestao: conversa.Sugestao | None,
    nomes_das_provas: Mapping[str, str],
) -> dict[str, tuple[str, ...]]:
    """Cursos sugeridos a que falta uma prova, com as notas atuais: chave -> nomes das provas (US37)."""
    if not estado.usar_notas or sugestao is None:
        return {}
    em_falta = notas.em_falta_por_curso([s.curso for s in sugestao.cursos], _notas_do_plano(db, user_id))
    return {chave: tuple(nomes_das_provas.get(p, p) for p in provas) for chave, provas in em_falta.items()}


def comecar(
    db: sqlite3.Connection,
    user_id: int,
    cliente: ClienteLLM,
    catalogo: Sequence[Curso],
    *,
    usar_notas: bool = False,
    nomes_das_provas: Mapping[str, str] | None = None,
) -> EstadoConversa:
    """Primeira pergunta do assistente. Se a conversa já começou, não faz nada.

    ``usar_notas`` é a autorização da pessoa (US37); só conta se ela tiver exames no plano.
    """
    estado = obter(db, user_id)
    if estado.comecada:
        return estado
    estado = EstadoConversa((), None, usar_notas and pode_usar_notas(db, user_id))
    return _pedir_ao_llm(db, user_id, estado, cliente, catalogo, nomes_das_provas=nomes_das_provas)


def validar_resposta(texto: str) -> str:
    texto = " ".join((texto or "").split())
    if not texto:
        raise RespostaVazia()
    if len(texto) > conversa.MAX_CARACTERES_RESPOSTA:
        raise RespostaLonga()
    return texto


def responder(
    db: sqlite3.Connection,
    user_id: int,
    texto: str,
    cliente: ClienteLLM,
    catalogo: Sequence[Curso],
    *,
    nomes_das_provas: Mapping[str, str] | None = None,
) -> EstadoConversa:
    """Guarda a resposta do aluno (sem dados pessoais) e pede a próxima pergunta ao LLM.

    A resposta é guardada antes de chamar o LLM: se ele falhar, a conversa não se perde e o
    aluno pode tentar de novo (``continuar``).
    """
    estado = obter(db, user_id)
    if not estado.comecada or estado.terminada or estado.a_espera_do_assistente:
        return estado
    limpo = remover_dados_pessoais(validar_resposta(texto))
    estado = EstadoConversa(estado.mensagens + (Mensagem("utilizador", limpo),), None, estado.usar_notas)
    _guardar(db, user_id, estado)
    return _pedir_ao_llm(db, user_id, estado, cliente, catalogo, nomes_das_provas=nomes_das_provas)


def continuar(
    db: sqlite3.Connection,
    user_id: int,
    cliente: ClienteLLM,
    catalogo: Sequence[Curso],
    *,
    nomes_das_provas: Mapping[str, str] | None = None,
) -> EstadoConversa:
    """Tenta de novo depois de o LLM ter falhado."""
    estado = obter(db, user_id)
    if not estado.a_espera_do_assistente:
        return estado
    return _pedir_ao_llm(
        db, user_id, estado, cliente, catalogo, forcar_sugestao=estado.sugestao_foi_pedida, nomes_das_provas=nomes_das_provas
    )


def pedir_sugestao(
    db: sqlite3.Connection,
    user_id: int,
    cliente: ClienteLLM,
    catalogo: Sequence[Curso],
    *,
    nomes_das_provas: Mapping[str, str] | None = None,
) -> EstadoConversa:
    """«Ver sugestões já» (US30): o pedido fica na conversa e o LLM tem de sugerir, sem mais perguntas.

    Como em ``responder``, o pedido é guardado antes de chamar o LLM: se ele falhar, «Tentar de
    novo» volta a pedir as sugestões.
    """
    estado = obter(db, user_id)
    if not estado.pode_pedir_sugestao:
        return estado
    estado = EstadoConversa(
        estado.mensagens + (Mensagem("utilizador", texts.ORIENTACAO_PEDIDO_SUGESTAO),), None, estado.usar_notas
    )
    _guardar(db, user_id, estado)
    return _pedir_ao_llm(db, user_id, estado, cliente, catalogo, forcar_sugestao=True, nomes_das_provas=nomes_das_provas)


def cursos_sugeridos(estado: EstadoConversa, catalogo: Sequence[Curso]) -> conversa.Sugestao | None:
    """Os cursos a mostrar, com os dados atuais do catálogo e a explicação do LLM.

    Volta a validar contra o catálogo (RN09): se um curso sair do catálogo depois de sugerido,
    deixa de aparecer.
    """
    if not estado.terminada:
        return None
    return conversa.validar_contra_catalogo(estado.sugestao, catalogo)


def continuar_conversa(db: sqlite3.Connection, user_id: int) -> EstadoConversa:
    """Com menos de 2 cursos sugeridos, o aluno pode continuar a conversa para dar mais pistas.

    A conversa mantém-se; a sugestão é apagada e a próxima resposta volta a pedir cursos ao LLM.
    Com sugestões suficientes não faz nada: a escolha do curso é a US31.
    """
    estado = obter(db, user_id)
    if not estado.terminada or estado.sugestao_suficiente:
        return estado
    novo = EstadoConversa(estado.mensagens, None, estado.usar_notas)
    _guardar(db, user_id, novo)
    return novo


def recomecar(db: sqlite3.Connection, user_id: int) -> None:
    repository.apagar(db, user_id)


def tem_sugestao(db: sqlite3.Connection, user_id: int) -> bool:
    """A conversa terminou com pelo menos 2 cursos: o percurso passa a «Escolher curso»."""
    return obter(db, user_id).sugestao_suficiente
