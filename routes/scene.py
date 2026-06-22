from flask import (
    Blueprint, Response, flash, redirect, render_template,
    request, session, url_for,
)

scene_bp = Blueprint("scene", __name__)

@scene_bp.route("/scene")
def scene():
    return render_template("scene.html")
