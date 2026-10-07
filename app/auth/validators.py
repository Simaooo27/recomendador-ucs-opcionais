"""Regras de validação do registo (US01). Funções puras, sem Flask nem base de dados."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .. import texts

# Parte local sem "@"; domínio com pelo menos um ponto. Comprimento máximo 254 (RFC 5321).
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+$")
_MAX_EMAIL_LENGTH = 254

# As mensagens vêm de app/texts.py; estes nomes mantêm-se para o resto do código e os testes.
MSG_EMAIL_REQUIRED = texts.ERROR_EMAIL_REQUIRED
MSG_PASSWORD_REQUIRED = texts.ERROR_PASSWORD_REQUIRED
MSG_PASSWORD_COMPOSITION = texts.ERROR_PASSWORD_COMPOSITION
MSG_PASSWORD_MISMATCH = texts.ERROR_PASSWORD_MISMATCH
MSG_PRIVACY_REQUIRED = texts.ERROR_PRIVACY_REQUIRED
MSG_EMAIL_DUPLICATE = texts.ERROR_EMAIL_DUPLICATE


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


def domains_hint(allowed_domains: Iterable[str]) -> str:
    """Texto com os domínios aceites, por exemplo «@iscap.ipp.pt»."""
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
        errors["email"] = texts.ERROR_EMAIL_DOMAIN.format(dominios=domains_hint(allowed_domains))

    password = data.password
    if not password:
        errors["password"] = MSG_PASSWORD_REQUIRED
    elif len(password) < min_length:
        errors["password"] = texts.ERROR_PASSWORD_TOO_SHORT.format(minimo=min_length)
    elif len(password) > max_length:
        errors["password"] = texts.ERROR_PASSWORD_TOO_LONG.format(maximo=max_length)
    elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        errors["password"] = MSG_PASSWORD_COMPOSITION

    if "password" not in errors and data.password_confirm != password:
        errors["password_confirm"] = MSG_PASSWORD_MISMATCH

    if not data.accepted_privacy:
        errors["accepted_privacy"] = MSG_PRIVACY_REQUIRED

    return errors
