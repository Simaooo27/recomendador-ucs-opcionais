"""Tokens assinados e com validade, sem estado no servidor.

- Confirmação de email (US01).
- Recuperar a palavra-passe (US47): o token leva uma impressão da palavra-passe atual. Quando a
  palavra-passe muda, a impressão deixa de bater certo e o token deixa de servir (uso único).
"""
from __future__ import annotations

import hashlib
import hmac

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

_SALT = "email-confirmation"
_SALT_RECUPERAR = "password-reset"


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


def impressao_da_password(secret_key: str, password_hash: str) -> str:
    """Um resumo do hash da palavra-passe, que muda sempre que a palavra-passe muda.

    Vai no token de recuperação e na sessão (US47). Não é o hash: com ele não se consegue
    adivinhar a palavra-passe, e o cookie de sessão pode ser lido no navegador.
    """
    return hmac.new(secret_key.encode(), password_hash.encode(), hashlib.sha256).hexdigest()[:32]


def make_reset_token(secret_key: str, user_id: int, impressao: str) -> str:
    return URLSafeTimedSerializer(secret_key, salt=_SALT_RECUPERAR).dumps({"uid": user_id, "p": impressao})


def read_reset_token(secret_key: str, token: str, max_age_seconds: int) -> tuple[int, str]:
    """Devolve ``(user_id, impressão)`` ou levanta ``TokenExpired`` / ``TokenInvalid``."""
    try:
        data = URLSafeTimedSerializer(secret_key, salt=_SALT_RECUPERAR).loads(token, max_age=max_age_seconds)
    except SignatureExpired as exc:
        raise TokenExpired from exc
    except BadSignature as exc:
        raise TokenInvalid from exc
    if not isinstance(data, dict) or not isinstance(data.get("uid"), int) or not isinstance(data.get("p"), str):
        raise TokenInvalid
    return data["uid"], data["p"]
