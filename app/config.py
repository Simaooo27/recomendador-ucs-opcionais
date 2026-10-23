"""Configuração da aplicação.

Os valores são lidos das variáveis de ambiente no momento em que a aplicação é
criada (e não ao importar o módulo), para que os testes possam sobrepor-se.
"""
from __future__ import annotations

import os


def _catalogo_por_omissao() -> str:
    dados = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")
    completo = os.path.join(dados, "catalogo-cursos.csv")
    return completo if os.path.exists(completo) else os.path.join(dados, "catalogo-cursos-mvp.csv")


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
        # Catálogo de cursos (dados públicos da DGES). Por omissão, o catálogo completo gerado por
        # dados/recolher_dges.py (US04); se ainda não existir, o do MVP (30 cursos).
        "CATALOGO_CSV": os.environ.get("CATALOGO_CSV") or _catalogo_por_omissao(),
        # LLM (spike da US30; ver app/llm/fabrica.py e docs/geral/05-spike-llm.md).
        # "falso" por omissão: quem clona o projeto corre tudo sem chaves nem rede.
        "LLM_BACKEND": os.environ.get("LLM_BACKEND", "falso"),
        "LLM_MODELO": os.environ.get("LLM_MODELO", ""),
        "LLM_TIMEOUT": float(os.environ.get("LLM_TIMEOUT", "15")),   # RNF12: resposta em menos de 15 s
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
        # Pedidos ao LLM por aluno e por dia (UTC). O limite do fornecedor é partilhado por todos;
        # este impede que uma só conta o gaste. 0 = sem limite.
        "ORIENTACAO_MAX_PEDIDOS_DIA": int(os.environ.get("ORIENTACAO_MAX_PEDIDOS_DIA", "40")),
        # Email
        "MAIL_BACKEND": os.environ.get("MAIL_BACKEND", "console"),
        "MAIL_SERVER": os.environ.get("MAIL_SERVER", ""),
        "MAIL_PORT": int(os.environ.get("MAIL_PORT", "587")),
        "MAIL_USE_TLS": _env_bool("MAIL_USE_TLS", True),
        "MAIL_USERNAME": os.environ.get("MAIL_USERNAME", ""),
        "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD", ""),
        "MAIL_SENDER": os.environ.get("MAIL_SENDER", "noreply@localhost"),
        # Com MAIL_BACKEND=console, a ligação de confirmação aparece também na página «Confirme o seu
        # email» (útil em desenvolvimento). Com «false», só aparece no terminal da aplicação: quem
        # entra pelo túnel deixa de conseguir confirmar emails que não são seus.
        "SHOW_DEV_CONFIRMATION_LINK": _env_bool("SHOW_DEV_CONFIRMATION_LINK", True),
        # Sessão / cookies
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_SECURE": _env_bool("SESSION_COOKIE_SECURE", False),
    }
