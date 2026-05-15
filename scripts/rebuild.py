"""Rebuild the database and GeoJSON files from scratch."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ["scripts/build_db.py", "scripts/generate_geojson.py"]


def main():
    for script in SCRIPTS:
        print(f">>> python {script}")
        result = subprocess.run([sys.executable, ROOT / script], cwd=ROOT)
        if result.returncode != 0:
            print(f"Failed at {script}.")
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
