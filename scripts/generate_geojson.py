"""Generate per-country GeoJSON files from the admin-1 shapefile.

Each country gets its own GeoJSON file. Countries with two-level subdivisions
get two files: {CODE}_1.geojson (dissolved regions) and {CODE}_2.geojson
(original subdivisions). Single-level countries get {CODE}.geojson.
Also generates a world.geojson from the admin-0 file for the homepage map.
"""

import sqlite3
from pathlib import Path

import geopandas as gpd
from shapely.affinity import translate
from shapely.geometry import MultiPolygon, Polygon

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
GEOJSON_DIR = DATA_DIR / "geojson"
DB_PATH = DATA_DIR / "subdivisions.db"

ADMIN0_SHP = RAW_DIR / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"
ADMIN1_SHP = (
    RAW_DIR
    / "ne_10m_admin_1_states_provinces"
    / "ne_10m_admin_1_states_provinces.shp"
)

from corrections import REGION_OVERRIDES


def generate_world_geojson(admin0_path: Path, output_path: Path) -> None:
    """Generate a lightweight world.geojson for the homepage map."""
    print("Generating world.geojson...")
    gdf = gpd.read_file(admin0_path)

    keep = ["NAME", "ADM0_A3", "ISO_A2", "geometry"]
    available = [c for c in keep if c in gdf.columns]
    gdf = gdf[available].copy()
    gdf = gdf.rename(columns={"NAME": "name", "ADM0_A3": "adm0_a3", "ISO_A2": "iso_a2"})

    gdf.geometry = gdf.geometry.simplify(tolerance=0.1, preserve_topology=True)

    gdf.to_file(output_path, driver="GeoJSON")
    size_kb = output_path.stat().st_size / 1024
    print(f"  world.geojson: {size_kb:.0f} KB")


def _unwrap_ring(coords: list) -> list:
    """Adjust ring vertices so no two consecutive vertices are > 180° apart.

    This keeps a polygon that crosses the antimeridian on one side of the map
    (with coordinates outside the normal -180/180 range) rather than splitting it.
    """
    result = []
    prev_x = None
    for coord in coords:
        x = coord[0]
        if prev_x is not None:
            while x - prev_x > 180:
                x -= 360
            while prev_x - x > 180:
                x += 360
        result.append((x,) + coord[1:])
        prev_x = x
    return result


def _unwrap_polygon(polygon: Polygon) -> Polygon:
    exterior = _unwrap_ring(list(polygon.exterior.coords))
    interiors = [_unwrap_ring(list(ring.coords)) for ring in polygon.interiors]
    return Polygon(exterior, interiors)


def fix_antimeridian(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Unwrap geometries that cross the antimeridian so they render as one
    contiguous shape on the correct side of the map.

    Each polygon part is shifted (by ±360°) to be within 180° of the largest
    polygon in the geometry, keeping everything on one side of the map.
    """
    def fix_geom(geom):
        if geom is None:
            return None
        if geom.geom_type == "Polygon":
            return _unwrap_polygon(geom)
        if geom.geom_type == "MultiPolygon":
            parts = list(geom.geoms)
            anchor_x = max(parts, key=lambda p: p.area).centroid.x
            result = []
            for poly in parts:
                cx = poly.centroid.x
                if cx - anchor_x > 180:
                    poly = translate(poly, xoff=-360)
                elif anchor_x - cx > 180:
                    poly = translate(poly, xoff=360)
                result.append(_unwrap_polygon(poly))
            return MultiPolygon(result)
        return geom

    gdf = gdf.copy()
    gdf["geometry"] = gdf["geometry"].apply(fix_geom)
    return gdf


def add_label_points(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Add label_lat and label_lon columns using representative_point()."""
    rep = gdf.geometry.representative_point()
    gdf["label_lon"] = rep.x
    gdf["label_lat"] = rep.y
    return gdf


def generate_country_geojsons(admin1_path: Path, output_dir: Path, db_path: Path) -> None:
    """Generate GeoJSON files per country, with separate files per level for two-level countries."""
    print(f"Reading admin-1 shapefile: {admin1_path}")
    gdf = gpd.read_file(admin1_path)

    # Ensure CRS is WGS84
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        print("  Reprojecting to EPSG:4326...")
        gdf = gdf.to_crs("EPSG:4326")

    # Filter out junk records
    gdf = gdf[~gdf["adm1_code"].str.contains(r"[\+\?~]", na=True)].copy()
    gdf = gdf[gdf["name"].notna() | gdf["name_en"].notna()].copy()

    # Prefer name_en over name
    gdf["name"] = gdf["name_en"].fillna(gdf["name"])

    conn = sqlite3.connect(db_path)
    # Get country info including has_levels flag
    countries = {}
    for row in conn.execute("SELECT adm0_a3, id, has_levels FROM countries").fetchall():
        countries[row[0]] = {"id": row[1], "has_levels": row[2]}

    generated = 0
    for code, group in gdf.groupby("adm0_a3"):
        if code not in countries:
            continue

        has_levels = countries[code]["has_levels"]

        if has_levels:
            # --- Level 2: original subdivisions ---
            output_cols = ["name", "adm1_code", "iso_3166_2", "type_en", "geometry"]
            available = [c for c in output_cols if c in group.columns]
            export2 = group[available].copy()
            export2 = add_label_points(export2)
            export2 = fix_antimeridian(export2)
            out_path_2 = output_dir / f"{code}_2.geojson"
            export2.to_file(out_path_2, driver="GeoJSON")

            # --- Level 1: dissolve by region ---
            region_col = "region"
            if region_col in group.columns:
                with_region = group.copy()
                # Apply manual overrides before falling back to the shapefile value
                override_mask = with_region["adm1_code"].isin(REGION_OVERRIDES)
                with_region.loc[override_mask, region_col] = (
                    with_region.loc[override_mask, "adm1_code"].map(REGION_OVERRIDES)
                )
                # Fall back to the feature's own name when region is still null
                with_region["region_name"] = with_region[region_col].fillna(with_region["name"]).astype(str).str.strip()

                dissolved = with_region.dissolve(by="region_name", as_index=False)
                # Create a synthetic adm1_code for each region
                dissolved["adm1_code"] = dissolved["region_name"].apply(
                    lambda r: f"{code}-R-{r.replace(' ', '_')[:30]}"
                )
                dissolved["name"] = dissolved["region_name"]
                dissolved["type_en"] = "region"

                keep_cols = ["name", "adm1_code", "type_en", "geometry"]
                dissolved = dissolved[keep_cols].copy()
                dissolved = add_label_points(dissolved)
                dissolved = fix_antimeridian(dissolved)

                out_path_1 = output_dir / f"{code}_1.geojson"
                dissolved.to_file(out_path_1, driver="GeoJSON")

            generated += 2
        else:
            # --- Single level ---
            output_cols = ["name", "adm1_code", "iso_3166_2", "type_en", "geometry"]
            available = [c for c in output_cols if c in group.columns]
            export = group[available].copy()
            export = add_label_points(export)
            export = fix_antimeridian(export)

            out_path = output_dir / f"{code}.geojson"
            export.to_file(out_path, driver="GeoJSON")
            generated += 1

    conn.close()
    print(f"  Generated {generated} GeoJSON files")


def main() -> None:
    if not ADMIN1_SHP.exists():
        print(f"Error: Shapefile not found at {ADMIN1_SHP}")
        print("Run download_data.py first.")
        return

    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        print("Run build_db.py first.")
        return

    GEOJSON_DIR.mkdir(parents=True, exist_ok=True)

    generate_world_geojson(ADMIN0_SHP, GEOJSON_DIR / "world.geojson")
    generate_country_geojsons(ADMIN1_SHP, GEOJSON_DIR, DB_PATH)

    print("\nGeoJSON generation complete.")


if __name__ == "__main__":
    main()
