from __future__ import annotations

from flask import Flask
import os
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
csrf_protect = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Basic, secure defaults; in production use env vars
    secret = os.getenv("FLASK_SECRET_KEY") or app.config.get("SECRET_KEY")
    if not secret:
        secret = secrets.token_hex(32)
    app.config["SECRET_KEY"] = secret
    app.config.setdefault("WTF_CSRF_SECRET_KEY", secret)

    # Database config (override with env var DATABASE_URL)
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/flask_blog",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    csrf_protect.init_app(app)

    # Register routes
    from .run import register_routes

    register_routes(app)

    return app

