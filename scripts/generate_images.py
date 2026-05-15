"""Generate per-subdivision PNG images for Anki cards.

Each image shows the country's outline with all subdivisions in light gray,
and the target subdivision highlighted in red. Used on Anki flashcards.

Usage:
    python scripts/generate_images.py              # All countries
    python scripts/generate_images.py --country USA # Single country
"""

import argparse
import sqlite3
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")  # Headless backend - must be before pyplot import
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
IMAGE_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "subdivisions.db"

ADMIN1_SHP = (
    RAW_DIR
    / "ne_10m_admin_1_states_provinces"
    / "ne_10m_admin_1_states_provinces.shp"
)

# Image settings
IMG_WIDTH = 400
IMG_HEIGHT = 300
DPI = 100
BG_COLOR = "#e0e0e0"      # Light gray for other subdivisions
HIGHLIGHT_COLOR = "#e84545"  # Red for the target subdivision
BORDER_COLOR = "#666666"
LINE_WIDTH = 0.5


def generate_country_images(
    country_code: str,
    country_gdf: gpd.GeoDataFrame,
    conn: sqlite3.Connection,
) -> int:
    """Generate images for all subdivisions of a country. Returns count generated."""
    country_dir = IMAGE_DIR / country_code
    country_dir.mkdir(parents=True, exist_ok=True)

    # Get country_id and subdivision info from DB
    row = conn.execute(
        "SELECT id FROM countries WHERE adm0_a3 = ?", (country_code,)
    ).fetchone()
    if not row:
        return 0
    country_id = row[0]

    generated = 0
    for idx, target_row in country_gdf.iterrows():
        adm1_code = target_row.get("adm1_code")
        if not adm1_code:
            continue

        # Use adm1_code as filename (ASCII-safe)
        safe_name = adm1_code.replace("/", "_").replace("\\", "_")
        img_path = country_dir / f"{safe_name}.png"

        # Skip if already generated
        if img_path.exists():
            continue

        fig, ax = plt.subplots(1, 1, figsize=(IMG_WIDTH / DPI, IMG_HEIGHT / DPI), dpi=DPI)

        # Plot all subdivisions in gray
        country_gdf.plot(
            ax=ax,
            color=BG_COLOR,
            edgecolor=BORDER_COLOR,
            linewidth=LINE_WIDTH,
        )

        # Highlight the target subdivision
        gpd.GeoDataFrame([target_row], crs=country_gdf.crs).plot(
            ax=ax,
            color=HIGHLIGHT_COLOR,
            edgecolor=BORDER_COLOR,
            linewidth=LINE_WIDTH * 1.5,
        )

        ax.set_axis_off()
        fig.tight_layout(pad=0.1)
        fig.savefig(img_path, dpi=DPI, bbox_inches="tight", pad_inches=0.05)
        plt.close(fig)

        # Update DB with image path
        rel_path = f"data/images/{country_code}/{safe_name}.png"
        conn.execute(
            "UPDATE subdivisions SET image_path = ? WHERE adm1_code = ?",
            (rel_path, adm1_code),
        )
        generated += 1

    conn.commit()
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate subdivision images for Anki cards")
    parser.add_argument(
        "--country",
        type=str,
        help="Generate images for a single country (3-letter code, e.g. USA)",
    )
    args = parser.parse_args()

    if not ADMIN1_SHP.exists():
        print(f"Error: Shapefile not found at {ADMIN1_SHP}")
        print("Run download_data.py first.")
        return

    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        print("Run build_db.py first.")
        return

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Reading admin-1 shapefile: {ADMIN1_SHP}")
    gdf = gpd.read_file(ADMIN1_SHP)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")

    if args.country:
        # Single country mode
        code = args.country.upper()
        country_gdf = gdf[gdf["adm0_a3"] == code]
        if country_gdf.empty:
            print(f"Error: No data found for country code '{code}'")
            conn.close()
            return
        print(f"Generating images for {code} ({len(country_gdf)} subdivisions)...")
        count = generate_country_images(code, country_gdf, conn)
        print(f"  Generated {count} images")
    else:
        # All countries
        countries = conn.execute(
            "SELECT adm0_a3, name, sub_count FROM countries ORDER BY name"
        ).fetchall()
        total = 0
        for i, (code, name, sub_count) in enumerate(countries, 1):
            country_gdf = gdf[gdf["adm0_a3"] == code]
            if country_gdf.empty:
                continue
            print(f"  [{i}/{len(countries)}] {name} ({sub_count} subdivisions)...", end="", flush=True)
            count = generate_country_images(code, country_gdf, conn)
            total += count
            print(f" {count} new")
        print(f"\nTotal: {total} images generated")

    conn.close()
    print("Image generation complete.")


if __name__ == "__main__":
    main()
