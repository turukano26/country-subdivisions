from pathlib import Path

from flask import Flask

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = str(DATA_DIR / "subdivisions.db")
    app.config["GEOJSON_DIR"] = str(DATA_DIR / "geojson")
    app.config["IMAGE_DIR"] = str(DATA_DIR / "images")
    app.config["DECKS_DIR"] = str(DATA_DIR / "decks")

    # Ensure decks dir exists
    (DATA_DIR / "decks").mkdir(parents=True, exist_ok=True)

    from .routes import home, country, deck

    app.register_blueprint(home.bp)
    app.register_blueprint(country.bp)
    app.register_blueprint(deck.bp)

    from . import db

    db.init_app(app)

    return app
