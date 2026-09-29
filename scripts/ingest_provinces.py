import urllib.request
import json
import subprocess
import sys

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'}

def fetch_geojson():
    # Attempt 1: Query geoBoundaries API for the direct CDN link (bypasses Git LFS pointer)
    print("Querying geoBoundaries API for South Africa provincial data...")
    try:
        api_url = "https://www.geoboundaries.org/api/current/gbOpen/ZAF/ADM1/"
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            meta = json.loads(resp.read().decode('utf-8'))
            dl_url = meta.get("simplifiedGeometryGeoJSON") or meta.get("gjDownloadURL")
            if dl_url:
                print(f"Downloading spatial features from CDN: {dl_url}")
                dl_req = urllib.request.Request(dl_url, headers=headers)
                with urllib.request.urlopen(dl_req, timeout=30) as dl_resp:
                    return json.loads(dl_resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Primary API notice ({e}). Trying fallback sources...")

    # Fallback mirrors
    fallbacks = [
        "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/south-africa.geojson",
        "https://raw.githubusercontent.com/RyzorBent/za-geojson/master/provinces.json"
    ]
    for url in fallbacks:
        try:
            print(f"Downloading from mirror: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if "features" in data:
                    return data
        except Exception as e:
            print(f"Mirror failed ({e})...")

    raise RuntimeError("All boundary data download sources failed.")

try:
    geojson_data = fetch_geojson()
except Exception as err:
    print(f"Fatal error: {err}")
    sys.exit(1)

features = geojson_data.get("features", [])
print(f"Successfully retrieved {len(features)} boundary features. Preparing PostGIS ingestion...")

sql_commands = [
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
    "CREATE INDEX IF NOT EXISTS idx_provinces_geom ON boundaries.provinces USING GIST (geom);"
]

for f in features:
    props = f.get("properties", {})
    name = props.get("shapeName") or props.get("name") or props.get("PROVINCE") or props.get("Province") or "Unknown"
    name = name.replace("'", "''").strip()
    
    code = props.get("shapeISO") or props.get("shapeID") or props.get("code") or props.get("CODE") or f"ZA-{name[:2].upper()}"
    code = code.replace("'", "''").strip()
    
    geom = f.get("geometry")
    if not geom:
        continue
    geom_str = json.dumps(geom).replace("'", "''")

    sql = f"""
    INSERT INTO boundaries.provinces (province_code, province_name, geom)
    VALUES (
        '{code}',
        '{name}',
        ST_Multi(ST_CollectionExtract(ST_MakeValid(ST_SetSRID(ST_GeomFromGeoJSON('{geom_str}'), 4326)), 3))
    )
    ON CONFLICT (province_name) DO UPDATE
    SET province_code = EXCLUDED.province_code,
        geom = EXCLUDED.geom;
    """
    sql_commands.append(sql)

sql_commands.append("COMMIT;")
full_sql = "\n".join(sql_commands)

print("Streaming geometries into PostGIS container...")
proc = subprocess.run(
    ["docker", "exec", "-i", "inqaba-postgres", "psql", "-U", "inqaba_admin", "-d", "inqaba_yesizwe"],
    input=full_sql.encode('utf-8'),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

if proc.returncode == 0:
    print("Stage 11 provincial boundary ingestion completed successfully.")
else:
    print("Ingestion error:", proc.stderr.decode('utf-8'))
