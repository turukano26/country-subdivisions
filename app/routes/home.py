from pathlib import Path

from flask import Blueprint, current_app, render_template, send_file

from ..db import get_db

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    db = get_db()
    countries = db.execute(
        "SELECT adm0_a3, name, subdivision_type, sub_count FROM countries ORDER BY name"
    ).fetchall()
    return render_template("home.html", countries=countries)


@bp.route("/api/world.geojson")
def world_geojson():
    path = Path(current_app.config["GEOJSON_DIR"]) / "world.geojson"
    return send_file(path, mimetype="application/json", max_age=0)
