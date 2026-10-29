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
from .tokens import (
    TokenExpired,
    TokenInvalid,
    impressao_da_password,
    make_confirmation_token,
    make_reset_token,
    read_confirmation_token,
    read_reset_token,
)
from .validators import (
    MSG_EMAIL_DUPLICATE,
    RegistrationInput,
    nome_error,
    normalize_email,
    normalize_nome,
    password_errors,
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
    nome: str = ""


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
    data = replace(data, email=normalize_email(data.email), nome=normalize_nome(data.nome))
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
                db, email=data.email, nome=data.nome, password_hash=password_hash, nonce=nonce, privacy_version=version, now=now
            )
        else:
            user_id = int(existing["id"])
            repository.refresh_pending_user(
                db, user_id=user_id, nome=data.nome, password_hash=password_hash, nonce=nonce, privacy_version=version, now=now
            )
        db.commit()
    except sqlite3.IntegrityError as exc:  # corrida: outro pedido criou o mesmo email entretanto
        db.rollback()
        raise RegistrationRejected({"email": MSG_EMAIL_DUPLICATE}) from exc

    token = make_confirmation_token(config["SECRET_KEY"], user_id, nonce)
    return PendingConfirmation(user_id=user_id, email=data.email, token=token, nome=data.nome)


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


def delete_account(db: sqlite3.Connection, user_id: int, password: str) -> bool:
    """Apaga a conta do aluno e todos os dados ligados a ela (US17).

    Pede a palavra-passe como confirmação: devolve False (e não apaga nada) se estiver errada.
    """
    user = repository.get_by_id(db, user_id)
    if user is None or not password or not check_password_hash(user["password_hash"], password):
        return False
    repository.delete_user(db, user_id)
    return True


def confirma_password(db: sqlite3.Connection, user_id: int, password: str) -> bool:
    """A palavra-passe está certa (confirmação de uma ação sensível, como exportar os dados, US46)."""
    user = repository.get_by_id(db, user_id)
    return user is not None and bool(password) and check_password_hash(user["password_hash"], password)


def change_nome(db: sqlite3.Connection, user_id: int, raw: str) -> str | None:
    """Muda o nome da conta. Devolve a mensagem de erro, ou ``None`` se mudou."""
    nome = normalize_nome(raw)
    erro = nome_error(nome)
    if erro is None:
        repository.update_nome(db, user_id, nome)
    return erro


# ---------------------------------------------------------------------------
# Recuperar a palavra-passe (US47)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PedidoDeRecuperacao:
    email: str
    nome: str
    token: str


def pedir_recuperacao(db: sqlite3.Connection, email: str, config: Mapping) -> PedidoDeRecuperacao | None:
    """O token para a ligação de recuperação, ou ``None`` se não há conta ativa com este email.

    A rota mostra a mesma mensagem nos dois casos, para não revelar que emails têm conta. Uma
    conta por confirmar não recebe ligação: primeiro tem de confirmar o email (US01).
    """
    user = repository.get_by_email(db, normalize_email(email))
    if user is None or not user["is_active"]:
        return None
    impressao = impressao_da_password(config["SECRET_KEY"], user["password_hash"])
    token = make_reset_token(config["SECRET_KEY"], int(user["id"]), impressao)
    return PedidoDeRecuperacao(email=user["email"], nome=user["nome"], token=token)


class RecuperacaoOutcome(str, Enum):
    VALID = "valid"
    INVALID = "invalid"      # adulterada, de outra conta, ou já usada (a palavra-passe já mudou)
    EXPIRED = "expired"      # passou mais de 1 hora


def _ler_token_de_recuperacao(db: sqlite3.Connection, token: str, config: Mapping) -> tuple[RecuperacaoOutcome, sqlite3.Row | None]:
    try:
        user_id, impressao = read_reset_token(config["SECRET_KEY"], token, config["RESET_TOKEN_MAX_AGE_SECONDS"])
    except TokenExpired:
        return RecuperacaoOutcome.EXPIRED, None
    except TokenInvalid:
        return RecuperacaoOutcome.INVALID, None
    user = repository.get_by_id(db, user_id)
    if user is None or not user["is_active"]:
        return RecuperacaoOutcome.INVALID, None
    atual = impressao_da_password(config["SECRET_KEY"], user["password_hash"])
    if not hmac.compare_digest(atual.encode(), impressao.encode()):
        return RecuperacaoOutcome.INVALID, None
    return RecuperacaoOutcome.VALID, user


def verificar_recuperacao(db: sqlite3.Connection, token: str, config: Mapping) -> RecuperacaoOutcome:
    """Se a ligação ainda serve (antes de mostrar o formulário da palavra-passe nova)."""
    return _ler_token_de_recuperacao(db, token, config)[0]


class RecuperacaoRejeitada(Exception):
    """A palavra-passe nova não cumpre as regras. ``errors`` mapeia campo -> mensagem."""

    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__(errors)
        self.errors = errors


def recuperar_password(
    db: sqlite3.Connection, token: str, password: str, password_confirm: str, config: Mapping
) -> RecuperacaoOutcome:
    """Muda a palavra-passe, se a ligação servir e a palavra-passe nova cumprir as regras.

    Ao mudar, a ligação deixa de servir (uso único) e as sessões abertas da conta terminam: as
    duas coisas dependem da impressão da palavra-passe (app/auth/tokens.py, app/auth/sessions.py).
    """
    outcome, user = _ler_token_de_recuperacao(db, token, config)
    if outcome is not RecuperacaoOutcome.VALID:
        return outcome
    errors = password_errors(
        password, password_confirm, min_length=config["PASSWORD_MIN_LENGTH"], max_length=config["PASSWORD_MAX_LENGTH"]
    )
    if errors:
        raise RecuperacaoRejeitada(errors)
    repository.update_password(db, int(user["id"]), generate_password_hash(password))
    return RecuperacaoOutcome.VALID
