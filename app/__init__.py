"""OptaBem: aplicação web (Flask) que ajuda a escolher o curso."""
from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template

from . import db, manuscrito, texts
from .config import default_config
from .mailer import create_mailer
from .security import init_security


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.update(default_config())
    if config:
        app.config.update(config)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY não definida. Defina a variável de ambiente SECRET_KEY (ver .env.example)."
        )
    if app.debug and app.config.get("SESSION_COOKIE_SECURE"):
        # SESSION_COOKIE_SECURE=true é o sinal de um site aberto a outras pessoas (por exemplo, pelo
        # túnel). Com --debug, o depurador do Flask permite executar código a partir de uma página
        # de erro: não pode estar ligado (docs/geral/06-aceder-noutro-dispositivo.md).
        raise RuntimeError(
            "Modo debug ligado com SESSION_COOKIE_SECURE=true. Para abrir o site a outras pessoas, "
            "arranque sem --debug (ver docs/geral/06-aceder-noutro-dispositivo.md)."
        )
    if not app.config.get("DATABASE"):
        app.config["DATABASE"] = str(Path(app.instance_path) / "app.sqlite3")

    if app.config.get("SESSION_COOKIE_SECURE"):
        # Pelo túnel do Cloudflare (SESSION_COOKIE_SECURE=true), o Flask recebe os pedidos em
        # http://localhost. Para as ligações completas (partilhar o plano, confirmar o email)
        # terem o endereço https://….trycloudflare.com, lê-se o endereço que o túnel indica.
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    db.init_app(app)
    from .gestao import cli as gestao_cli

    gestao_cli.init_app(app)
    from .orientacao import cli as orientacao_cli

    orientacao_cli.init_app(app)
    init_security(app)
    app.extensions["mailer"] = create_mailer(app.config)

    from .auth import bp as auth_bp
    from .candidatura.routes import bp as candidatura_bp
    from .catalogo import bp as catalogo_bp
    from .gestao import bp as gestao_bp
    from .main import bp as main_bp
    from .orientacao import bp as orientacao_bp
    from .percurso.routes import bp as percurso_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalogo_bp)
    app.register_blueprint(orientacao_bp)
    app.register_blueprint(percurso_bp)
    app.register_blueprint(candidatura_bp)
    app.register_blueprint(gestao_bp, url_prefix=app.config["ADMIN_URL_PREFIX"])

    # Todos os templates recebem os textos de app/texts.py como «texts».
    @app.context_processor
    def _inject_texts():
        return {"texts": texts, "manuscrito": manuscrito.desenhar}

    @app.errorhandler(400)
    @app.errorhandler(404)
    def _client_error(error):
        return render_template("error.html", error=error), error.code

    return app
