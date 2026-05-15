"""Parse Natural Earth shapefiles and populate the SQLite database.

Reads the admin-0 (countries) and admin-1 (states/provinces) shapefiles,
then inserts structured data into subdivisions.db.

Countries where the shapefile contains second-level subdivisions (e.g. France's
departments, Italy's provinces) are detected via the 'region' field. For these
countries, dissolved level-1 entries are also created.
"""

import math
import sqlite3
from collections import Counter
from pathlib import Path

import geopandas as gpd


def clean_str(val) -> str | None:
    """Convert a shapefile field value to a clean string, or None if empty/NaN."""
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    s = str(val).strip()
    if not s or s == "-99":
        return None
    return s

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "subdivisions.db"

ADMIN0_SHP = RAW_DIR / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"
ADMIN1_SHP = (
    RAW_DIR
    / "ne_10m_admin_1_states_provinces"
    / "ne_10m_admin_1_states_provinces.shp"
)

from corrections import DEFAULT_LEVEL_1, REGION_OVERRIDES

MIN_SUBDIVISIONS = 2  # Skip countries with fewer than this many subdivisions

# Thresholds for detecting two-level countries
MIN_REGIONS = 5         # Country must have at least this many distinct regions
MIN_LEVEL_RATIO = 2.5   # At least 2.5x more subs than regions

SCHEMA = """
CREATE TABLE IF NOT EXISTS countries (
    id              INTEGER PRIMARY KEY,
    adm0_a3         TEXT UNIQUE NOT NULL,
    iso_a2          TEXT,
    name            TEXT NOT NULL,
    name_short      TEXT,
    subdivision_type TEXT,
    geojson_path    TEXT,
    sub_count       INTEGER DEFAULT 0,
    has_levels      INTEGER DEFAULT 0,
    default_level   INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS subdivisions (
    id              INTEGER PRIMARY KEY,
    country_id      INTEGER NOT NULL REFERENCES countries(id),
    adm1_code       TEXT UNIQUE NOT NULL,
    iso_3166_2      TEXT,
    name            TEXT NOT NULL,
    name_local      TEXT,
    type            TEXT,
    type_en         TEXT,
    image_path      TEXT,
    level           INTEGER NOT NULL DEFAULT 1,
    no_parent       INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_subdivisions_country ON subdivisions(country_id);
CREATE INDEX IF NOT EXISTS idx_subdivisions_level ON subdivisions(country_id, level);

CREATE TABLE IF NOT EXISTS decks (
    id              INTEGER PRIMARY KEY,
    country_id      INTEGER UNIQUE NOT NULL REFERENCES countries(id),
    apkg_path       TEXT,
    generated_at    TEXT,
    card_count      INTEGER
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def load_admin1(path: Path) -> gpd.GeoDataFrame:
    print(f"Reading admin-1 shapefile: {path}")
    gdf = gpd.read_file(path)
    print(f"  {len(gdf)} subdivision records loaded")
    return gdf


def normalize_type(raw_type) -> str:
    """Normalize subdivision type to lowercase English."""
    cleaned = clean_str(raw_type)
    if not cleaned:
        return "subdivision"
    return cleaned.lower()


def get_modal_type(types: list[str]) -> str:
    """Return the most common type for a country's subdivisions."""
    counter = Counter(types)
    return counter.most_common(1)[0][0] if counter else "subdivision"


def build_country_lookup(admin0_path: Path) -> dict[str, dict]:
    """Build a lookup from adm0_a3 -> country info from the admin-0 shapefile."""
    print(f"Reading admin-0 shapefile: {admin0_path}")
    gdf = gpd.read_file(admin0_path)
    lookup = {}
    for _, row in gdf.iterrows():
        code = clean_str(row.get("ADM0_A3")) or clean_str(row.get("adm0_a3"))
        if code:
            lookup[code] = {
                "name": clean_str(row.get("NAME")) or clean_str(row.get("name")) or code,
                "name_short": clean_str(row.get("NAME_LONG")) or clean_str(row.get("name_long")),
                "iso_a2": clean_str(row.get("ISO_A2")) or clean_str(row.get("iso_a2")),
            }
    print(f"  {len(lookup)} countries in admin-0 lookup")
    return lookup


def is_junk_record(row) -> bool:
    """Filter out placeholder/junk records from Natural Earth data."""
    adm1_code = clean_str(row.get("adm1_code")) or ""
    if any(ch in adm1_code for ch in "+?~"):
        return True
    if not clean_str(row.get("name")) and not clean_str(row.get("name_en")):
        return True
    return False


def get_region(row) -> str | None:
    """Return the region for a row, applying manual overrides before the shapefile value."""
    adm1_code = clean_str(row.get("adm1_code"))
    if adm1_code and adm1_code in REGION_OVERRIDES:
        return REGION_OVERRIDES[adm1_code]
    return clean_str(row.get("region"))


def best_name(row) -> str:
    """Pick the best available name, preferring name_en over name."""
    return clean_str(row.get("name_en")) or clean_str(row.get("name")) or "Unknown"


def detect_two_level_countries(grouped: dict) -> dict[str, list[str]]:
    """Detect countries where the 'region' field provides a meaningful higher-level grouping.

    Returns a dict of {country_code: [list of unique region names]}.
    """
    two_level = {}
    for code, rows in grouped.items():
        regions = set()
        for r in rows:
            region = get_region(r) or best_name(r)
            regions.add(region)

        n_regions = len(regions)
        n_subs = len(rows)

        if n_regions >= MIN_REGIONS and n_subs / n_regions >= MIN_LEVEL_RATIO:
            two_level[code] = sorted(regions)

    return two_level


def populate(conn: sqlite3.Connection, admin1: gpd.GeoDataFrame, country_lookup: dict) -> None:
    """Insert countries and subdivisions into the database."""
    # Group subdivisions by country code, filtering out junk
    grouped = {}
    skipped = 0
    for _, row in admin1.iterrows():
        code = clean_str(row.get("adm0_a3"))
        if not code:
            continue
        if is_junk_record(row):
            skipped += 1
            continue
        grouped.setdefault(code, []).append(row)

    print(f"  Filtered out {skipped} junk/placeholder records")

    # Detect countries with two-level subdivisions
    two_level = detect_two_level_countries(grouped)
    print(f"  Detected {len(two_level)} countries with two-level subdivisions")

    countries_inserted = 0
    subdivisions_inserted = 0
    level1_inserted = 0

    for code, rows in sorted(grouped.items()):
        if len(rows) < MIN_SUBDIVISIONS:
            continue

        has_levels = code in two_level

        # Collect types for this country
        types = [normalize_type(r.get("type_en") or r.get("type")) for r in rows]
        modal_type = get_modal_type(types)

        # Get country name from admin-0 lookup, fall back to admin-1's 'admin' field
        info = country_lookup.get(code, {})
        country_name = info.get("name") or clean_str(rows[0].get("admin")) or code

        default_level = 1 if (has_levels and code in DEFAULT_LEVEL_1) else (2 if has_levels else 1)
        if has_levels:
            sub_count = len(two_level[code]) if default_level == 1 else len(rows)
        else:
            sub_count = len(rows)

        conn.execute(
            """INSERT OR REPLACE INTO countries
               (adm0_a3, iso_a2, name, name_short, subdivision_type, sub_count, has_levels, default_level)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                code,
                info.get("iso_a2"),
                country_name,
                info.get("name_short"),
                modal_type,
                sub_count,
                1 if has_levels else 0,
                default_level,
            ),
        )
        country_id = conn.execute(
            "SELECT id FROM countries WHERE adm0_a3 = ?", (code,)
        ).fetchone()[0]
        countries_inserted += 1

        # Determine the level for these subdivisions
        level = 2 if has_levels else 1

        # Detect duplicate names and disambiguate by appending the type
        name_counts = Counter(best_name(r) for r in rows)
        duped_names = {n for n, c in name_counts.items() if c > 1}

        # Insert subdivisions from the shapefile
        for row, type_en in zip(rows, types):
            adm1_code = clean_str(row.get("adm1_code")) or f"{code}-{best_name(row)}"
            iso_3166_2 = clean_str(row.get("iso_3166_2"))
            name = best_name(row)
            name_local = clean_str(row.get("name_local"))
            raw_type = clean_str(row.get("type")) or clean_str(row.get("type_en"))
            no_parent = 1 if (has_levels and not get_region(row)) else 0

            # Disambiguate duplicate names by appending the type
            if name in duped_names and raw_type:
                name = f"{name} ({raw_type})"

            conn.execute(
                """INSERT OR REPLACE INTO subdivisions
                   (country_id, adm1_code, iso_3166_2, name, name_local, type, type_en, level, no_parent)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (country_id, adm1_code, iso_3166_2, name, name_local, raw_type, type_en, level, no_parent),
            )
            subdivisions_inserted += 1

        # For two-level countries, also insert level-1 regions
        if has_levels:
            region_names = two_level[code]
            # Figure out the type name for level-1 regions
            # Use the most common region-level type from the data if available
            region_type = "region"  # sensible default
            for region_name in region_names:
                synth_code = f"{code}-R-{region_name.replace(' ', '_')[:30]}"
                conn.execute(
                    """INSERT OR REPLACE INTO subdivisions
                       (country_id, adm1_code, name, type, type_en, level)
                       VALUES (?, ?, ?, ?, ?, 1)""",
                    (country_id, synth_code, region_name, region_type.title(), region_type),
                )
                level1_inserted += 1

    conn.commit()
    print(f"  Inserted {countries_inserted} countries")
    print(f"  Inserted {subdivisions_inserted} level-2/single-level subdivisions")
    print(f"  Inserted {level1_inserted} level-1 regions (dissolved)")


def main() -> None:
    if not ADMIN1_SHP.exists():
        print(f"Error: Shapefile not found at {ADMIN1_SHP}")
        print("Run download_data.py first.")
        return

    # Remove old DB if exists
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed old database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    print("Initializing database schema...")
    init_db(conn)

    country_lookup = build_country_lookup(ADMIN0_SHP)
    admin1 = load_admin1(ADMIN1_SHP)

    print("Populating database...")
    populate(conn, admin1, country_lookup)

    # Print summary
    cur = conn.cursor()
    n_countries = cur.execute("SELECT COUNT(*) FROM countries").fetchone()[0]
    n_subs = cur.execute("SELECT COUNT(*) FROM subdivisions").fetchone()[0]
    n_l1 = cur.execute("SELECT COUNT(*) FROM subdivisions WHERE level = 1").fetchone()[0]
    n_l2 = cur.execute("SELECT COUNT(*) FROM subdivisions WHERE level = 2").fetchone()[0]
    n_multi = cur.execute("SELECT COUNT(*) FROM countries WHERE has_levels = 1").fetchone()[0]
    print(f"\nDatabase ready: {DB_PATH}")
    print(f"  {n_countries} countries ({n_multi} with multiple levels)")
    print(f"  {n_subs} total subdivisions ({n_l1} level-1, {n_l2} level-2)")

    # Show two-level countries
    print("\nTwo-level countries:")
    for row in cur.execute(
        """SELECT c.name, c.adm0_a3,
                  (SELECT COUNT(*) FROM subdivisions s WHERE s.country_id = c.id AND s.level = 1) as l1,
                  (SELECT COUNT(*) FROM subdivisions s WHERE s.country_id = c.id AND s.level = 2) as l2
           FROM countries c WHERE c.has_levels = 1 ORDER BY c.name"""
    ):
        print(f"  {row[0]:30s} ({row[1]}): {row[2]} regions, {row[3]} subdivisions")

    conn.close()


if __name__ == "__main__":
    main()
