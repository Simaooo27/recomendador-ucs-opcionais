"""Casos de uso das contas: registar aluno e confirmar email (US01), autenticar (US02)."""
from __future__ import annotations

import hmac
import secrets
import sqlite3
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping

from werkzeug.security import check_password_hash, generate_password_hash

from . import repository
from .tokens import TokenExpired, TokenInvalid, make_confirmation_token, read_confirmation_token
from .validators import (
    MSG_EMAIL_DUPLICATE,
    RegistrationInput,
    normalize_email,
    validate_registration,
)


class RegistrationRejected(Exception):
    """Os dados do registo não são válidos. ``errors`` mapeia campo -> mensagem."""

    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__(errors)
        self.errors = errors


@dataclass(frozen=True)
class PendingConfirmation:
    user_id: int
    email: str
    token: str


class LoginOutcome(str, Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    INACTIVE = "inactive"


@dataclass(frozen=True)
class LoginResult:
    outcome: LoginOutcome
    user_id: int | None = None


# Hash usado quando o email não existe, para a verificação demorar o mesmo tempo
# e não revelar que emails estão registados.
_DUMMY_PASSWORD_HASH = generate_password_hash("palavra-passe-que-nao-existe")


class ConfirmationOutcome(str, Enum):
    CONFIRMED = "confirmed"
    ALREADY_CONFIRMED = "already_confirmed"
    INVALID = "invalid"
    EXPIRED = "expired"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def register_student(db: sqlite3.Connection, data: RegistrationInput, config: Mapping) -> PendingConfirmation:
    """Valida os dados e cria (ou renova) uma conta **inativa**.

    - Email já ativo: rejeita.
    - Email já registado mas por confirmar: atualiza a palavra-passe e gera um novo
      token (as ligações anteriores deixam de funcionar).
    """
    data = replace(data, email=normalize_email(data.email))
    errors = validate_registration(
        data,
        allowed_domains=config["ALLOWED_EMAIL_DOMAINS"],
        min_length=config["PASSWORD_MIN_LENGTH"],
        max_length=config["PASSWORD_MAX_LENGTH"],
    )
    if errors:
        raise RegistrationRejected(errors)

    existing = repository.get_by_email(db, data.email)
    if existing is not None and existing["is_active"]:
        raise RegistrationRejected({"email": MSG_EMAIL_DUPLICATE})

    password_hash = generate_password_hash(data.password)
    nonce = secrets.token_urlsafe(16)
    now = _utc_now()
    version = config["PRIVACY_POLICY_VERSION"]

    try:
        if existing is None:
            user_id = repository.create_user(
                db, email=data.email, password_hash=password_hash, nonce=nonce, privacy_version=version, now=now
            )
        else:
            user_id = int(existing["id"])
            repository.refresh_pending_user(
                db, user_id=user_id, password_hash=password_hash, nonce=nonce, privacy_version=version, now=now
            )
        db.commit()
    except sqlite3.IntegrityError as exc:  # corrida: outro pedido criou o mesmo email entretanto
        db.rollback()
        raise RegistrationRejected({"email": MSG_EMAIL_DUPLICATE}) from exc

    token = make_confirmation_token(config["SECRET_KEY"], user_id, nonce)
    return PendingConfirmation(user_id=user_id, email=data.email, token=token)


def confirm_email(db: sqlite3.Connection, token: str, config: Mapping) -> ConfirmationOutcome:
    """Ativa a conta associada ao token. É idempotente para contas já ativas."""
    try:
        user_id, nonce = read_confirmation_token(
            config["SECRET_KEY"], token, config["CONFIRMATION_TOKEN_MAX_AGE_SECONDS"]
        )
    except TokenExpired:
        return ConfirmationOutcome.EXPIRED
    except TokenInvalid:
        return ConfirmationOutcome.INVALID

    user = repository.get_by_id(db, user_id)
    if user is None or not hmac.compare_digest(user["confirmation_nonce"].encode(), nonce.encode()):
        return ConfirmationOutcome.INVALID
    if user["is_active"]:
        return ConfirmationOutcome.ALREADY_CONFIRMED

    repository.activate_user(db, user_id, _utc_now())
    db.commit()
    return ConfirmationOutcome.CONFIRMED


def authenticate(db: sqlite3.Connection, email: str, password: str) -> LoginResult:
    """Verifica email e palavra-passe (US02).

    - Email inexistente ou palavra-passe errada: ``INVALID_CREDENTIALS`` (a mesma resposta
      nos dois casos, para não revelar que emails têm conta).
    - Palavra-passe certa mas conta por confirmar: ``INACTIVE``.
    """
    user = repository.get_by_email(db, normalize_email(email))
    if user is None:
        check_password_hash(_DUMMY_PASSWORD_HASH, password)
        return LoginResult(LoginOutcome.INVALID_CREDENTIALS)
    if not password or not check_password_hash(user["password_hash"], password):
        return LoginResult(LoginOutcome.INVALID_CREDENTIALS)
    if not user["is_active"]:
        return LoginResult(LoginOutcome.INACTIVE)
    return LoginResult(LoginOutcome.SUCCESS, user_id=int(user["id"]))
