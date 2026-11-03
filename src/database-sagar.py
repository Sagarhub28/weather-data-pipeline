import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from config import settings

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def connect(db_path=None):
    path = Path(db_path or settings.DATABASE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def setup_database(db_path=None):
    schema = Path(__file__).resolve().parents[1] / "database/schema.sql"
    conn = connect(db_path)
    try:
        conn.executescript(schema.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


def upsert_city(conn, city):
    name, country = city["city_name"].strip(), city.get("country_code", "").strip().upper()
    conn.execute("INSERT INTO cities(city_name,country_code,latitude,longitude) VALUES(?,?,?,?) "
                 "ON CONFLICT(city_name,country_code) DO UPDATE SET "
                 "latitude=COALESCE(excluded.latitude,cities.latitude), "
                 "longitude=COALESCE(excluded.longitude,cities.longitude)",
                 (name,country,city.get("latitude"),city.get("longitude")))
    return conn.execute("SELECT city_id FROM cities WHERE city_name=? AND country_code=?",
                        (name,country)).fetchone()["city_id"]

def insert_observation(conn, city_id, o):
    cur = conn.execute("INSERT OR IGNORE INTO weather_observations "
        "(city_id,observed_at,fetched_at,temperature_c,feels_like_c,humidity_percent,pressure_hpa,"
        "wind_speed_mps,weather_main,weather_description,source) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (city_id,o["observed_at"],o["fetched_at"],o["temperature_c"],o.get("feels_like_c"),
         o["humidity_percent"],o["pressure_hpa"],o["wind_speed_mps"],o["weather_main"],
         o["weather_description"],o.get("source","openweathermap")))
    return cur.rowcount == 1

def start_run(conn, city_id, started):
    return conn.execute("INSERT INTO pipeline_runs(city_id,started_at,status) VALUES(?,?,'running')",
                        (city_id,started)).lastrowid

def finish_run(conn, run_id, status, completed, count=0, error=None):
    conn.execute("UPDATE pipeline_runs SET status=?,completed_at=?,records_processed=?,error_message=? WHERE run_id=?",
                 (status,completed,count,error,run_id))
