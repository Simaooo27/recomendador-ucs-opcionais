"""Regras de validação do registo (US01). Funções puras, sem Flask nem base de dados."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

# Parte local sem "@"; domínio com pelo menos um ponto. Comprimento máximo 254 (RFC 5321).
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+$")
_MAX_EMAIL_LENGTH = 254

MSG_EMAIL_REQUIRED = "Indique o seu email institucional."
MSG_PASSWORD_REQUIRED = "Escolha uma palavra-passe."
MSG_PASSWORD_COMPOSITION = "A palavra-passe deve incluir pelo menos uma letra e um número."
MSG_PASSWORD_MISMATCH = "As palavras-passe não coincidem."
MSG_PRIVACY_REQUIRED = "É necessário aceitar a política de privacidade para criar a conta."
MSG_EMAIL_DUPLICATE = "Já existe uma conta com este email. Se é a sua, inicie sessão."


@dataclass(frozen=True)
class RegistrationInput:
    email: str
    password: str
    password_confirm: str
    accepted_privacy: bool


def normalize_email(raw: str) -> str:
    """Remove espaços nas pontas e passa para minúsculas."""
    return raw.strip().lower()


def is_institutional_email(email: str, allowed_domains: Iterable[str]) -> bool:
    """True se o email é válido e o domínio é (ou é subdomínio de) um domínio permitido.

    ``evil-iscap.ipp.pt`` e ``iscap.ipp.pt.evil.com`` são rejeitados: só se aceita o
    domínio exato ou um subdomínio verdadeiro (``alunos.iscap.ipp.pt``).
    """
    email = normalize_email(email)
    if len(email) > _MAX_EMAIL_LENGTH or not _EMAIL_RE.match(email):
        return False
    domain = email.rsplit("@", 1)[1]
    return any(domain == d or domain.endswith("." + d) for d in (x.lower() for x in allowed_domains))


def _domains_hint(allowed_domains: Iterable[str]) -> str:
    return " ou ".join("@" + d for d in allowed_domains)


def validate_registration(
    data: RegistrationInput,
    *,
    allowed_domains: list[str],
    min_length: int,
    max_length: int,
) -> dict[str, str]:
    """Devolve ``{campo: mensagem}``; dicionário vazio se tudo estiver válido.

    Espera que ``data.email`` já esteja normalizado (ver ``normalize_email``).
    """
    errors: dict[str, str] = {}

    if not data.email:
        errors["email"] = MSG_EMAIL_REQUIRED
    elif not is_institutional_email(data.email, allowed_domains):
        errors["email"] = f"Use o seu email institucional (terminado em {_domains_hint(allowed_domains)})."

    password = data.password
    if not password:
        errors["password"] = MSG_PASSWORD_REQUIRED
    elif len(password) < min_length:
        errors["password"] = f"A palavra-passe deve ter pelo menos {min_length} caracteres."
    elif len(password) > max_length:
        errors["password"] = f"A palavra-passe não pode ter mais de {max_length} caracteres."
    elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        errors["password"] = MSG_PASSWORD_COMPOSITION

    if "password" not in errors and data.password_confirm != password:
        errors["password_confirm"] = MSG_PASSWORD_MISMATCH

    if not data.accepted_privacy:
        errors["accepted_privacy"] = MSG_PRIVACY_REQUIRED

    return errors
