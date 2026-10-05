"""Recomendador de UCs opcionais: aplicação web (Flask)."""
from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template

from . import db
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
    if not app.config.get("DATABASE"):
        app.config["DATABASE"] = str(Path(app.instance_path) / "app.sqlite3")

    db.init_app(app)
    init_security(app)
    app.extensions["mailer"] = create_mailer(app.config)

    from .auth import bp as auth_bp
    from .main import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @app.errorhandler(400)
    @app.errorhandler(404)
    def _client_error(error):
        return render_template("error.html", error=error), error.code

    return app
