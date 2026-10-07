"""Configuração da aplicação.

Os valores são lidos das variáveis de ambiente no momento em que a aplicação é
criada (e não ao importar o módulo), para que os testes possam sobrepor-se.
"""
from __future__ import annotations

import os


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "sim", "on"}


def _env_list(name: str, default: str) -> list[str]:
    raw = os.environ.get(name, default)
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


def default_config() -> dict:
    return {
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "DATABASE": os.environ.get("DATABASE_PATH"),
        # Registo (US01)
        # Vazio (por omissão) = aceita qualquer email. Para exigir um domínio, ex.: "iscap.ipp.pt".
        "ALLOWED_EMAIL_DOMAINS": _env_list("ALLOWED_EMAIL_DOMAINS", ""),
        "PASSWORD_MIN_LENGTH": 8,
        "PASSWORD_MAX_LENGTH": 128,
        "CONFIRMATION_TOKEN_MAX_AGE_SECONDS": 24 * 60 * 60,
        "PRIVACY_POLICY_VERSION": "1.0",
        # Área de gestão (US03): endereço sem ligações nas páginas dos alunos. Pode ser mudado.
        "ADMIN_URL_PREFIX": "/" + os.environ.get("ADMIN_URL_PREFIX", "gestao").strip("/"),
        # Email
        "MAIL_BACKEND": os.environ.get("MAIL_BACKEND", "console"),
        "MAIL_SERVER": os.environ.get("MAIL_SERVER", ""),
        "MAIL_PORT": int(os.environ.get("MAIL_PORT", "587")),
        "MAIL_USE_TLS": _env_bool("MAIL_USE_TLS", True),
        "MAIL_USERNAME": os.environ.get("MAIL_USERNAME", ""),
        "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD", ""),
        "MAIL_SENDER": os.environ.get("MAIL_SENDER", "noreply@localhost"),
        # Sessão / cookies
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_SECURE": _env_bool("SESSION_COOKIE_SECURE", False),
    }
