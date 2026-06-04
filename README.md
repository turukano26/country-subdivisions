# Country Subdivisions

An interactive web app for exploring country subdivisions and generating Anki decks to memorize them.

## Running the app

```
poetry run flask --app app run --port 5000 --debug
```

Then open http://localhost:5000 in your browser.

## Setup

Install dependencies:

```
poetry install
```

Download the source data (Natural Earth shapefiles):

```
poetry run python scripts/download_data.py
```

Build the database and generate GeoJSON files:

```
poetry run python scripts/rebuild.py
```

## Data corrections

`scripts/corrections.py` is the single place to tweak how source data is interpreted:

- **`REGION_OVERRIDES`** — manually assign a level-1 region to subdivisions that are missing one in the Natural Earth data (keyed by `adm1_code`)
- **`DEFAULT_LEVEL_1`** — set of `adm0_a3` country codes that should show their higher-level regions by default instead of the more detailed subdivisions

After editing `corrections.py`, rebuild with:

```
poetry run python scripts/rebuild.py
```
