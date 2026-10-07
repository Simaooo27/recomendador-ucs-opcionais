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
