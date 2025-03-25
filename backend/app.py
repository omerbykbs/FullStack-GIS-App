from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import List
import logging
import os
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


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


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,   
        port=DB_PORT,
        cursor_factory=RealDictCursor 
    )
    try:
        yield conn
    finally:
        conn.close()

class Location(BaseModel):
    name: str
    latitude: float
    longitude: float

@app.post("/locations/")
def add_location(location: Location, db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO locations (name, latitude, longitude, geom) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
                (location.name, location.latitude, location.longitude, location.longitude, location.latitude),
            )
            db.commit()
        return {"message": "Ort hinzugefügt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/locations/all/")
def get_all_locations(db=Depends(get_db)):
    try:
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = "SELECT name, latitude, longitude FROM locations;"
            cur.execute(query)
            results = cur.fetchall()
        if not results:
            return {"message": "No locations found"}
        return {"locations": results}
    except Exception as e:
        print("Error in get_all_locations:", e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/locations/nearby/")
def find_nearby_locations(lat: float, lon: float, radius_km: int = 5, db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            query = """
            SELECT name, latitude, longitude 
            FROM locations 
            WHERE ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s * 1000);
            """
            cur.execute(query, (lon, lat, radius_km))
            results = cur.fetchall()

        if not results:
            return {"message": "No locations found within the specified radius"}
        return {"nearby_locations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "Welcome to the GIS API!"}
