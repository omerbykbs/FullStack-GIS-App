import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Database credentials (Local)
#DB_NAME = "gisdb"
#DB_USER = "postgres"
#DB_PASSWORD = "root"
#DB_HOST = "localhost"
#DB_PORT = "5433"

# Database credentials (Docker)
DB_NAME = "gisdb"
DB_USER = "admin"
DB_PASSWORD = "root"
DB_HOST = "db"
DB_PORT = "5432"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    cursor_factory=RealDictCursor
)

with conn.cursor() as cur:
    with open("export.geojson") as f:
        geojson_data = json.load(f)
    
    for feature in geojson_data["features"]:
        props = feature["properties"]
        name = props.get("name")
        longitude, latitude = feature["geometry"]["coordinates"]
        cur.execute(
            "INSERT INTO locations (name, latitude, longitude, geom) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
            (name, latitude, longitude, longitude, latitude)
        )
    conn.commit()

conn.close()
