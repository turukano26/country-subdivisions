"""Download Natural Earth shapefiles for country boundaries and subdivisions.

Downloads:
- 110m admin-0 countries (small, used for the world map homepage)
- 10m admin-1 states/provinces (detailed, used for subdivision maps and data)
"""

import io
import sys
import zipfile
from pathlib import Path

import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

DOWNLOADS = {
    "ne_110m_admin_0_countries": (
        "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    ),
    "ne_10m_admin_1_states_provinces": (
        "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_1_states_provinces.zip"
    ),
}


def download_and_extract(name: str, url: str) -> None:
    dest = DATA_DIR / name
    if dest.exists() and any(dest.glob("*.shp")):
        print(f"  {name}/ already exists, skipping")
        return

    print(f"  Downloading {name}...")
    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()

    # Read into memory, then extract
    total = int(resp.headers.get("content-length", 0))
    buf = io.BytesIO()
    downloaded = 0
    for chunk in resp.iter_content(chunk_size=1024 * 256):
        buf.write(chunk)
        downloaded += len(chunk)
        if total:
            pct = downloaded * 100 // total
            print(f"\r  Downloading {name}... {pct}%", end="", flush=True)
    print()

    print(f"  Extracting {name}...")
    buf.seek(0)
    with zipfile.ZipFile(buf) as zf:
        dest.mkdir(parents=True, exist_ok=True)
        zf.extractall(dest)

    print(f"  Done: {dest}")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading Natural Earth shapefiles...")
    for name, url in DOWNLOADS.items():
        download_and_extract(name, url)
    print("\nAll downloads complete.")


if __name__ == "__main__":
    main()
