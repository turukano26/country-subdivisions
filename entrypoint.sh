#!/bin/sh
set -e

if [ ! -f /app/data/subdivisions.db ]; then
    echo "First run: downloading source data..."
    python scripts/download_data.py
    echo "Building database and GeoJSON files..."
    python scripts/rebuild.py
fi

exec gunicorn --bind 0.0.0.0:8083 "app:create_app()"
