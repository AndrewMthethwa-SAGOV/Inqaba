import json
import subprocess
import os

filepath = os.path.expanduser("~/inqaba/boundaries/provinces.geojson")

with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])
print(f"Loaded {len(features)} provincial boundaries from file.")

sql_lines = [
    "BEGIN;",
    "CREATE SCHEMA IF NOT EXISTS boundaries;",
    """
    CREATE TABLE IF NOT EXISTS boundaries.provinces (
        id SERIAL PRIMARY KEY,
        province_code VARCHAR(32),
        province_name VARCHAR(100) UNIQUE,
        geom GEOMETRY(MultiPolygon, 4326)
    );
    """,
    "TRUNCATE TABLE boundaries.provinces RESTART IDENTITY;"
]

for f in features:
    props = f.get("properties", {})
    name = props.get("name") or props.get("shapeName") or "Unknown"
    name = name.strip().replace("'", "''")
    code = f"ZA-{name[:2].upper()}"
    geom_str = json.dumps(f.get("geometry")).replace("'", "''")

    sql = f"""
    INSERT INTO boundaries.provinces (province_code, province_name, geom)
    VALUES (
        '{code}',
        '{name}',
        ST_Multi(ST_CollectionExtract(ST_MakeValid(ST_SetSRID(ST_GeomFromGeoJSON('{geom_str}'), 4326)), 3))
    );
    """
    sql_lines.append(sql)

sql_lines.append("CREATE INDEX IF NOT EXISTS idx_provinces_geom ON boundaries.provinces USING GIST (geom);")
sql_lines.append("COMMIT;")

full_sql = "\n".join(sql_lines)

proc = subprocess.run(
    ["docker", "exec", "-i", "inqaba-postgres", "psql", "-U", "inqaba_admin", "-d", "inqaba_yesizwe"],
    input=full_sql.encode("utf-8"),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

if proc.returncode == 0:
    print("All 9 South African provinces successfully committed to boundaries.provinces.")
else:
    print("PostGIS ingestion error:", proc.stderr.decode("utf-8"))
