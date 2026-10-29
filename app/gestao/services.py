"""Casos de uso dos administradores (US03): criar, autenticar e remover."""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping

from werkzeug.security import check_password_hash, generate_password_hash

from .. import texts
from . import repository

_USERNAME_RE = re.compile(r"^[a-z0-9._-]{3,30}$")
_DUMMY_PASSWORD_HASH = generate_password_hash("palavra-passe-que-nao-existe")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_username(raw: str) -> str:
    return raw.strip().lower()


def validate_new_admin(
    username: str, password: str, password_confirm: str, config: Mapping
) -> dict[str, str]:
    """Devolve ``{campo: mensagem}``; vazio se tudo estiver válido. Espera o nome já normalizado."""
    errors: dict[str, str] = {}
    if not username:
        errors["username"] = texts.ERROR_ADMIN_USERNAME_REQUIRED
    elif not _USERNAME_RE.match(username):
        errors["username"] = texts.ERROR_ADMIN_USERNAME_FORMAT
    minimum, maximum = config["PASSWORD_MIN_LENGTH"], config["PASSWORD_MAX_LENGTH"]
    if not password:
        errors["password"] = texts.ERROR_PASSWORD_REQUIRED
    elif len(password) < minimum:
        errors["password"] = texts.ERROR_PASSWORD_TOO_SHORT.format(minimo=minimum)
    elif len(password) > maximum:
        errors["password"] = texts.ERROR_PASSWORD_TOO_LONG.format(maximo=maximum)
    elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        errors["password"] = texts.ERROR_PASSWORD_COMPOSITION
    if "password" not in errors and password_confirm != password:
        errors["password_confirm"] = texts.ERROR_PASSWORD_MISMATCH
    return errors


class AdminRejected(Exception):
    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__(errors)
        self.errors = errors


def create_admin(
    db: sqlite3.Connection,
    username: str,
    password: str,
    password_confirm: str,
    config: Mapping,
    *,
    created_by: str | None,
) -> int:
    """Cria um administrador. ``created_by`` é o nome de quem o criou; vazio = criado no terminal."""
    username = normalize_username(username)
    errors = validate_new_admin(username, password, password_confirm, config)
    if not errors and repository.get_by_username(db, username) is not None:
        errors["username"] = texts.ERROR_ADMIN_USERNAME_TAKEN
    if errors:
        raise AdminRejected(errors)
    try:
        admin_id = repository.create(
            db, username=username, password_hash=generate_password_hash(password), now=_utc_now(), created_by=created_by
        )
        db.commit()
    except sqlite3.IntegrityError as exc:  # corrida: outro pedido criou o mesmo nome entretanto
        db.rollback()
        raise AdminRejected({"username": texts.ERROR_ADMIN_USERNAME_TAKEN}) from exc
    return admin_id


def authenticate(db: sqlite3.Connection, username: str, password: str) -> int | None:
    """Devolve o id do administrador se o nome e a palavra-passe estiverem certos; senão ``None``."""
    admin = repository.get_by_username(db, normalize_username(username))
    if admin is None:
        check_password_hash(_DUMMY_PASSWORD_HASH, password)  # mesmo tempo de resposta
        return None
    if not password or not check_password_hash(admin["password_hash"], password):
        return None
    repository.set_last_login(db, int(admin["id"]), _utc_now())
    db.commit()
    return int(admin["id"])


class RemoveOutcome(str, Enum):
    REMOVED = "removed"
    NOT_FOUND = "not_found"
    SELF = "self"  # um administrador não se remove a si próprio (garante que fica sempre um)


@dataclass(frozen=True)
class RemoveResult:
    outcome: RemoveOutcome
    username: str = ""


def remove_admin(db: sqlite3.Connection, admin_id: int, *, removed_by: int) -> RemoveResult:
    admin = repository.get_by_id(db, admin_id)
    if admin is None:
        return RemoveResult(RemoveOutcome.NOT_FOUND)
    if admin_id == removed_by:
        return RemoveResult(RemoveOutcome.SELF, admin["username"])
    repository.delete(db, admin_id)
    db.commit()
    return RemoveResult(RemoveOutcome.REMOVED, admin["username"])


@dataclass(frozen=True)
class Indicadores:
    """Números do painel de gestão (nunca dados de alunos individuais)."""

    alunos_ativos: int
    contas_por_confirmar: int
    administradores: int
    ultimo_registo: str | None  # data (AAAA-MM-DD) do registo mais recente


def indicadores(db: sqlite3.Connection) -> Indicadores:
    from ..auth import repository as alunos  # import local: evita dependência circular

    ativas, pendentes = alunos.count_by_status(db)
    ultimo = alunos.last_created_at(db)
    return Indicadores(ativas, pendentes, repository.count(db), ultimo[:10] if ultimo else None)


def ativar_conta(db: sqlite3.Connection, user_id: int) -> str | None:
    """Ativa uma conta de aluno por confirmar (enquanto o site não envia emails a sério, 23/10).

    Devolve o email da conta ativada, ou ``None`` se não existe ou já estava ativa.
    """
    from ..auth import repository as contas

    conta = contas.get_by_id(db, user_id)
    if conta is None or conta["is_active"]:
        return None
    contas.activate_user(db, user_id, _utc_now())
    db.commit()
    return conta["email"]


# ---------------------------------------------------------------------------
# Corrigir e esconder cursos do catálogo (US39)
# ---------------------------------------------------------------------------

LIMITE_DESCRICAO = 3000
LIMITE_SAIDAS = 1500


class CursoInexistente(LookupError):
    """Não há nenhum curso com este identificador no catálogo da DGES."""


class CorrecaoRejeitada(Exception):
    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__(errors)
        self.errors = errors


def normalizar_descricao(raw: str) -> str:
    """Um só parágrafo, como no CSV: espaços e mudanças de linha seguidos passam a um espaço."""
    return " ".join((raw or "").split())


def normalizar_saidas(raw: str) -> str:
    """Uma saída por linha ou separadas por «;» -> «A; B; C» (o formato do CSV)."""
    partes = [normalizar_descricao(p) for linha in (raw or "").splitlines() for p in linha.split(";")]
    return "; ".join(p for p in partes if p)


def _curso_da_dges(config: Mapping, chave: str):
    from ..catalogo import repository as catalogo

    curso = next((c for c in catalogo.todos(config["CATALOGO_CSV"]) if c.chave == chave), None)
    if curso is None:
        raise CursoInexistente(chave)
    return curso


def guardar_correcao(
    db: sqlite3.Connection, config: Mapping, chave: str, *, descricao: str, saidas: str, escondido: bool, admin: str
) -> tuple[str, ...]:
    """Guarda a correção de um curso e regista quem a fez e quando.

    Um campo vazio, ou igual ao da DGES, deixa de ser correção (fica o texto da DGES). Se não sobrar
    nada corrigido nem escondido, a linha sai da tabela. Devolve o que mudou (vazio se nada mudou).
    """
    from ..catalogo import correcoes_repository
    from ..catalogo.services import Correcao, correcoes

    original = _curso_da_dges(config, chave)
    descricao, saidas = normalizar_descricao(descricao), normalizar_saidas(saidas)
    errors: dict[str, str] = {}
    if len(descricao) > LIMITE_DESCRICAO:
        errors["descricao"] = texts.ADMIN_CURSO_ERRO_LONGO.format(maximo=LIMITE_DESCRICAO)
    if len(saidas) > LIMITE_SAIDAS:
        errors["saidas"] = texts.ADMIN_CURSO_ERRO_LONGO.format(maximo=LIMITE_SAIDAS)
    if errors:
        raise CorrecaoRejeitada(errors)

    nova_descricao = None if descricao in ("", normalizar_descricao(original.descricao)) else descricao
    novas_saidas = None if saidas in ("", normalizar_saidas(original.saidas)) else saidas
    atual = correcoes(db).get(chave, Correcao())
    alteracoes = []
    if nova_descricao != atual.descricao:
        alteracoes.append("descricao")
    if novas_saidas != atual.saidas:
        alteracoes.append("saidas")
    if escondido != atual.escondido:
        alteracoes.append("escondido" if escondido else "visivel")
    if not alteracoes:
        return ()

    agora = _utc_now()
    if nova_descricao is None and novas_saidas is None and not escondido:
        correcoes_repository.apagar(db, chave)
    else:
        correcoes_repository.guardar(
            db, chave, descricao=nova_descricao, saidas=novas_saidas, escondido=escondido, por=admin, em=agora
        )
    correcoes_repository.registar(db, chave, ",".join(alteracoes), admin, agora)
    db.commit()
    return tuple(alteracoes)


def repor_curso(db: sqlite3.Connection, config: Mapping, chave: str, *, admin: str) -> bool:
    """Volta aos dados da DGES (apaga a correção) e regista-o. Devolve False se não havia correção."""
    from ..catalogo import correcoes_repository

    _curso_da_dges(config, chave)
    if correcoes_repository.obter(db, chave) is None:
        return False
    agora = _utc_now()
    correcoes_repository.apagar(db, chave)
    correcoes_repository.registar(db, chave, "reposto", admin, agora)
    db.commit()
    return True


@dataclass(frozen=True)
class Alteracao:
    o_que: tuple[str, ...]   # códigos: descricao, saidas, escondido, visivel, reposto
    por: str
    em: str

    @property
    def resumo(self) -> str:
        """«descrição, saídas profissionais» (textos ADMIN_CURSO_O_QUE_* de app/texts.py)."""
        return ", ".join(getattr(texts, f"ADMIN_CURSO_O_QUE_{codigo.upper()}", codigo) for codigo in self.o_que)


def historico_do_curso(db: sqlite3.Connection, chave: str) -> list[Alteracao]:
    from ..catalogo import correcoes_repository

    return [
        Alteracao(tuple(linha["alteracao"].split(",")), linha["alterado_por"], linha["alterado_em"])
        for linha in correcoes_repository.historico(db, chave)
    ]
