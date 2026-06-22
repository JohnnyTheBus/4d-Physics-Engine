from flask import Blueprint, render_template, session, redirect, url_for, request

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
def homepage():
    return render_template("home.html")

@core_bp.route("/settings")
def settings():
    return render_template("settings.html")