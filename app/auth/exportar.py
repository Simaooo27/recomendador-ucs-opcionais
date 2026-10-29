"""Exportar os meus dados (US46): tudo o que o OptaBem guarda sobre um aluno, num ficheiro JSON.

Direito de acesso e de portabilidade (RGPD, RNF01). Ficam de fora:
- o hash da palavra-passe e o valor interno da confirmação do email (não são dados da pessoa,
  são proteções da conta, e com eles seria mais fácil atacá-la);
- o código da ligação de partilha do plano (quem o tem vê o plano): o ficheiro diz só se o plano
  está partilhado.

Só se leem linhas do próprio ``user_id`` (nunca há dados de outros utilizadores).
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Sequence

from ..catalogo.repository import Curso

# Muda se a forma do ficheiro mudar, para quem o ler noutro programa saber o que esperar.
VERSAO_DO_FORMATO = 1


def _json(valor: str | None, omissao: Any) -> Any:
    if not valor:
        return omissao
    try:
        return json.loads(valor)
    except ValueError:
        return omissao


def _conta(user: sqlite3.Row) -> dict:
    return {
        "nome": user["nome"],
        "email": user["email"],
        "criada_em": user["created_at"],
        "confirmada_em": user["confirmed_at"],
        "politica_de_privacidade": {"versao": user["privacy_policy_version"], "aceite_em": user["privacy_accepted_at"]},
    }


def _decisoes(linhas: Sequence[sqlite3.Row]) -> list[dict]:
    # Da mais antiga para a mais recente: é a ordem em que a pessoa as tomou.
    return [
        {
            "curso_chave": linha["curso_chave"],
            "curso": linha["curso"],
            "instituicao": linha["instituicao"],
            "origem": linha["origem"],
            "cursos_sugeridos_nessa_altura": _json(linha["sugeridos"], []),
            "decidida_em": linha["decidida_em"],
        }
        for linha in reversed(linhas)
    ]


def _candidatura(linha: sqlite3.Row | None, partilhado: bool, catalogo: Sequence[Curso]) -> dict | None:
    if linha is None:
        return None
    por_chave = {curso.chave: curso for curso in catalogo}
    opcoes = []
    for posicao, chave in enumerate(_json(linha["opcoes"], []), start=1):
        curso = por_chave.get(chave)
        opcoes.append({
            "posicao": posicao,
            "curso_chave": chave,
            # Um curso que saiu do catálogo continua na lista, só sem o nome.
            "curso": curso.curso if curso else None,
            "instituicao": curso.instituicao if curso else None,
        })
    return {
        "media_do_secundario": linha["media"],
        "exames": _json(linha["exames"], {}),   # código da prova -> nota de 0 a 200
        "opcoes": opcoes,
        "partilhado": partilhado,
        "atualizado_em": linha["atualizado_em"],
    }


def _conversa(linha: sqlite3.Row | None) -> dict | None:
    if linha is None:
        return None
    return {
        "mensagens": _json(linha["mensagens"], []),
        "sugestao": _json(linha["sugestao"], None),
        "atualizada_em": linha["atualizada_em"],
    }


def dados_do_utilizador(db: sqlite3.Connection, user_id: int, catalogo: Sequence[Curso]) -> dict | None:
    """Os dados de um aluno, prontos para ``json.dumps``. ``None`` se a conta não existir."""
    # Importados aqui: os pacotes da orientação e do percurso importam a autenticação ao arrancar.
    from ..candidatura import repository as candidatura
    from ..orientacao import repository as orientacao
    from ..percurso import repository as percurso
    from . import repository as contas

    user = contas.get_by_id(db, user_id)
    if user is None:
        return None
    return {
        "aplicacao": "OptaBem",
        "versao_do_formato": VERSAO_DO_FORMATO,
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "conta": _conta(user),
        "decisoes_do_percurso": _decisoes(percurso.listar(db, user_id)),
        "plano_de_candidatura": _candidatura(
            candidatura.obter(db, user_id), candidatura.partilha(db, user_id) is not None, catalogo
        ),
        "conversa_de_orientacao": _conversa(orientacao.obter(db, user_id)),
        "pedidos_ao_assistente_por_dia": [
            {"dia": linha["dia"], "total": linha["total"]} for linha in orientacao.pedidos_do_utilizador(db, user_id)
        ],
    }


def nome_do_ficheiro(agora: datetime | None = None) -> str:
    agora = agora or datetime.now(timezone.utc)
    return f"optabem-os-meus-dados-{agora:%Y-%m-%d}.json"
