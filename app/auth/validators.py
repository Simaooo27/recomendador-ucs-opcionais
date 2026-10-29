"""Regras de validação do registo (US01). Funções puras, sem Flask nem base de dados.

Por omissão aceita-se qualquer email válido (email pessoal). Se ``allowed_domains`` tiver
domínios, só se aceitam emails desses domínios (por exemplo, para voltar a exigir o
email institucional).
"""
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


_MAX_NOME_LENGTH = 60
# Letras (com acentos), espaços, hífen, apóstrofo e ponto: «Ana-Rita», «D'Almeida», «J. Silva».
_NOME_CARACTERES_EXTRA = set(" -'’.")


@dataclass(frozen=True)
class RegistrationInput:
    email: str
    password: str
    password_confirm: str
    accepted_privacy: bool
    nome: str = ""


def normalize_nome(raw: str) -> str:
    """Tira os espaços das pontas e junta os repetidos («  Ana   Rita » -> «Ana Rita»)."""
    return " ".join(raw.split())


def nome_error(nome: str) -> str | None:
    """Mensagem de erro do nome (já normalizado), ou ``None`` se é válido."""
    if not nome:
        return texts.ERROR_NOME_REQUIRED
    if len(nome) > _MAX_NOME_LENGTH or not any(c.isalpha() for c in nome):
        return texts.ERROR_NOME_INVALID.format(maximo=_MAX_NOME_LENGTH)
    if not all(c.isalpha() or c in _NOME_CARACTERES_EXTRA for c in nome):
        return texts.ERROR_NOME_INVALID.format(maximo=_MAX_NOME_LENGTH)
    return None


def primeiro_nome(nome: str) -> str:
    """A primeira palavra do nome, para a saudação («Duarte Eusébio» -> «Duarte»)."""
    partes = (nome or "").split()
    return partes[0] if partes else ""


def normalize_email(raw: str) -> str:
    """Remove espaços nas pontas e passa para minúsculas."""
    return raw.strip().lower()


def is_valid_email(email: str) -> bool:
    """True se o email tem um formato válido e não é demasiado longo."""
    email = normalize_email(email)
    return len(email) <= _MAX_EMAIL_LENGTH and bool(_EMAIL_RE.match(email))


def is_allowed_domain(email: str, allowed_domains: Iterable[str]) -> bool:
    """True se não há restrição de domínio ou se o domínio é (ou é subdomínio de) um permitido.

    ``evil-iscap.ipp.pt`` e ``iscap.ipp.pt.evil.com`` são rejeitados: só se aceita o
    domínio exato ou um subdomínio verdadeiro (``alunos.iscap.ipp.pt``).
    """
    domains = [d.lower() for d in allowed_domains]
    if not domains:
        return True
    domain = normalize_email(email).rsplit("@", 1)[1]
    return any(domain == d or domain.endswith("." + d) for d in domains)


def domains_hint(allowed_domains: Iterable[str]) -> str:
    """Texto com os domínios aceites, por exemplo «@iscap.ipp.pt»; vazio se não há restrição."""
    return " ou ".join("@" + d for d in allowed_domains)


def password_errors(password: str, password_confirm: str, *, min_length: int, max_length: int) -> dict[str, str]:
    """Regras da palavra-passe nova, no registo (US01) e ao recuperá-la (US47).

    Devolve ``{"password" | "password_confirm": mensagem}``; vazio se está válida.
    """
    errors: dict[str, str] = {}
    if not password:
        errors["password"] = MSG_PASSWORD_REQUIRED
    elif len(password) < min_length:
        errors["password"] = texts.ERROR_PASSWORD_TOO_SHORT.format(minimo=min_length)
    elif len(password) > max_length:
        errors["password"] = texts.ERROR_PASSWORD_TOO_LONG.format(maximo=max_length)
    elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        errors["password"] = MSG_PASSWORD_COMPOSITION

    if "password" not in errors and password_confirm != password:
        errors["password_confirm"] = MSG_PASSWORD_MISMATCH
    return errors


def validate_registration(
    data: RegistrationInput,
    *,
    allowed_domains: list[str],
    min_length: int,
    max_length: int,
) -> dict[str, str]:
    """Devolve ``{campo: mensagem}``; dicionário vazio se tudo estiver válido.

    Espera que ``data.email`` já esteja normalizado (ver ``normalize_email``).
    O nome é obrigatório desde 23/10 (decisão do PO: tratar a pessoa pelo nome).
    """
    errors: dict[str, str] = {}

    erro_nome = nome_error(normalize_nome(data.nome))
    if erro_nome:
        errors["nome"] = erro_nome

    if not data.email:
        errors["email"] = MSG_EMAIL_REQUIRED
    elif not is_valid_email(data.email):
        errors["email"] = texts.ERROR_EMAIL_INVALID
    elif not is_allowed_domain(data.email, allowed_domains):
        errors["email"] = texts.ERROR_EMAIL_DOMAIN.format(dominios=domains_hint(allowed_domains))

    errors.update(password_errors(data.password, data.password_confirm, min_length=min_length, max_length=max_length))

    if not data.accepted_privacy:
        errors["accepted_privacy"] = MSG_PRIVACY_REQUIRED

    return errors
