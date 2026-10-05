"""Tokens de confirmação de email: assinados e com validade, sem estado no servidor."""
from __future__ import annotations

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

_SALT = "email-confirmation"


class TokenInvalid(Exception):
    """Token adulterado, malformado ou com conteúdo inesperado."""


class TokenExpired(Exception):
    """Token válido mas fora do prazo."""


def _serializer(secret_key: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key, salt=_SALT)


def make_confirmation_token(secret_key: str, user_id: int, nonce: str) -> str:
    return _serializer(secret_key).dumps({"uid": user_id, "n": nonce})


def read_confirmation_token(secret_key: str, token: str, max_age_seconds: int) -> tuple[int, str]:
    """Devolve ``(user_id, nonce)`` ou levanta ``TokenExpired`` / ``TokenInvalid``."""
    try:
        data = _serializer(secret_key).loads(token, max_age=max_age_seconds)
    except SignatureExpired as exc:
        raise TokenExpired from exc
    except BadSignature as exc:
        raise TokenInvalid from exc
    if not isinstance(data, dict) or not isinstance(data.get("uid"), int) or not isinstance(data.get("n"), str):
        raise TokenInvalid
    return data["uid"], data["n"]
