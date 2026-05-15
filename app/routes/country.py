from pathlib import Path

from flask import Blueprint, abort, current_app, render_template, request, send_file

from ..db import get_db

bp = Blueprint("country", __name__)


@bp.route("/country/<adm0_a3>")
def detail(adm0_a3):
    adm0_a3 = adm0_a3.upper()
    db = get_db()

    country = db.execute(
        "SELECT * FROM countries WHERE adm0_a3 = ?", (adm0_a3,)
    ).fetchone()
    if not country:
        abort(404)

    has_levels = country["has_levels"]

    # Build subdivision data for each level
    levels = {}
    if has_levels:
        for lvl in (1, 2):
            subs = db.execute(
                """SELECT name, type, type_en, iso_3166_2, adm1_code
                   FROM subdivisions
                   WHERE country_id = ? AND level = ?
                   ORDER BY name""",
                (country["id"], lvl),
            ).fetchall()
            type_counts = {}
            for s in subs:
                t = s["type_en"] or "subdivision"
                type_counts[t] = type_counts.get(t, 0) + 1
            levels[lvl] = {"subdivisions": subs, "type_counts": type_counts}
    else:
        subs = db.execute(
            """SELECT name, type, type_en, iso_3166_2, adm1_code
               FROM subdivisions
               WHERE country_id = ?
               ORDER BY name""",
            (country["id"],),
        ).fetchall()
        type_counts = {}
        for s in subs:
            t = s["type_en"] or "subdivision"
            type_counts[t] = type_counts.get(t, 0) + 1
        levels[1] = {"subdivisions": subs, "type_counts": type_counts}

    return render_template(
        "country.html",
        country=country,
        levels=levels,
        has_levels=has_levels,
    )


@bp.route("/api/country/<adm0_a3>.geojson")
def country_geojson(adm0_a3):
    adm0_a3 = adm0_a3.upper()
    level = request.args.get("level", type=int)
    geojson_dir = Path(current_app.config["GEOJSON_DIR"])

    # Try level-specific file first, then plain
    if level:
        path = geojson_dir / f"{adm0_a3}_{level}.geojson"
    else:
        path = geojson_dir / f"{adm0_a3}.geojson"

    if not path.exists():
        # Fall back to plain file for single-level countries
        path = geojson_dir / f"{adm0_a3}.geojson"

    if not path.exists():
        abort(404)
    return send_file(path, mimetype="application/json", max_age=0)
