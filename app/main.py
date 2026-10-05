"""Páginas gerais."""
from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return redirect(url_for("auth.register_form"))


@bp.get("/privacidade")
def privacy():
    return render_template("privacy.html")
