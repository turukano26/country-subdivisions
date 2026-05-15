import hashlib
from datetime import datetime, timezone
from pathlib import Path

import genanki
from flask import Blueprint, abort, current_app, send_file

from ..db import get_db

bp = Blueprint("deck", __name__)


def stable_id(key: str) -> int:
    """Generate a stable integer ID from a string key (for genanki)."""
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)


CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    text-align: center;
    padding: 1.5rem;
    background: #f8f9fa;
    color: #1a1a2e;
}
.card img { max-width: 100%; height: auto; border-radius: 8px; margin: 1rem 0; }
.country-name { font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; }
.question { font-size: 1.3rem; font-weight: 600; margin: 0.5rem 0; }
.answer-name { font-size: 1.5rem; font-weight: 700; color: #e94560; margin: 0.5rem 0; }
.answer-type { font-size: 1rem; color: #666; }
"""


def build_model(country_code: str) -> genanki.Model:
    model_id = stable_id(f"{country_code}_model_v2")
    return genanki.Model(
        model_id,
        f"{country_code} Subdivisions",
        fields=[
            {"name": "CountryName"},
            {"name": "SubdivisionName"},
            {"name": "SubdivisionType"},
            {"name": "MapImage"},
        ],
        templates=[
            {
                "name": "Name This Subdivision",
                "qfmt": (
                    '<div class="country-name">{{CountryName}}</div>'
                    '<div class="question">What is the name of the highlighted {{SubdivisionType}}?</div>'
                    "{{MapImage}}"
                ),
                "afmt": (
                    '{{FrontSide}}<hr id="answer">'
                    '<div class="answer-name">{{SubdivisionName}}</div>'
                    '<div class="answer-type">{{SubdivisionType}}</div>'
                ),
            },
            {
                "name": "Locate This Subdivision",
                "qfmt": (
                    '<div class="country-name">{{CountryName}}</div>'
                    '<div class="question">Where is {{SubdivisionName}}?</div>'
                    '<div class="answer-type">({{SubdivisionType}})</div>'
                ),
                "afmt": (
                    '{{FrontSide}}<hr id="answer">'
                    "{{MapImage}}"
                    '<div class="answer-name">{{SubdivisionName}}</div>'
                ),
            },
        ],
        css=CSS,
    )


@bp.route("/country/<adm0_a3>/deck")
def download_deck(adm0_a3):
    adm0_a3 = adm0_a3.upper()
    db = get_db()

    country = db.execute(
        "SELECT * FROM countries WHERE adm0_a3 = ?", (adm0_a3,)
    ).fetchone()
    if not country:
        abort(404)

    subdivisions = db.execute(
        """SELECT name, type_en, adm1_code, image_path
           FROM subdivisions
           WHERE country_id = ?
           ORDER BY name""",
        (country["id"],),
    ).fetchall()
    if not subdivisions:
        abort(404)

    decks_dir = Path(current_app.config["DECKS_DIR"])
    apkg_path = decks_dir / f"{adm0_a3}.apkg"
    image_dir = Path(current_app.config["IMAGE_DIR"])

    # Check cache
    cached = db.execute(
        "SELECT apkg_path, generated_at FROM decks WHERE country_id = ?",
        (country["id"],),
    ).fetchone()
    if cached and apkg_path.exists():
        return send_file(
            apkg_path,
            as_attachment=True,
            download_name=f"{country['name']}_subdivisions.apkg",
        )

    # Generate deck
    model = build_model(adm0_a3)
    deck_id = stable_id(f"{adm0_a3}_deck")
    deck = genanki.Deck(deck_id, f"Geography::Subdivisions::{country['name']}")

    media_files = []
    for sub in subdivisions:
        sub_type = sub["type_en"] or "subdivision"
        adm1_code = sub["adm1_code"]
        safe_name = adm1_code.replace("/", "_").replace("\\", "_")

        img_file = image_dir / adm0_a3 / f"{safe_name}.png"
        if img_file.exists():
            media_files.append(str(img_file))
            img_tag = f'<img src="{safe_name}.png">'
        else:
            img_tag = "<em>(no map image)</em>"

        note = genanki.Note(
            model=model,
            fields=[
                country["name"],
                sub["name"],
                sub_type,
                img_tag,
            ],
            guid=genanki.guid_for(adm1_code),
        )
        deck.add_note(note)

    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    pkg.write_to_file(str(apkg_path))

    # Update cache
    db.execute(
        """INSERT OR REPLACE INTO decks (country_id, apkg_path, generated_at, card_count)
           VALUES (?, ?, ?, ?)""",
        (
            country["id"],
            str(apkg_path),
            datetime.now(timezone.utc).isoformat(),
            len(subdivisions),
        ),
    )
    db.commit()

    return send_file(
        apkg_path,
        as_attachment=True,
        download_name=f"{country['name']}_subdivisions.apkg",
    )
