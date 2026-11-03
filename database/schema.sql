PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS cities (
 city_id INTEGER PRIMARY KEY AUTOINCREMENT,
 city_name TEXT NOT NULL, country_code TEXT NOT NULL DEFAULT '',
 latitude REAL, longitude REAL,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
 UNIQUE(city_name, country_code)
);
CREATE TABLE IF NOT EXISTS weather_observations (
 observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
 city_id INTEGER NOT NULL, observed_at TEXT NOT NULL, fetched_at TEXT NOT NULL,
 temperature_c REAL NOT NULL, feels_like_c REAL,
 humidity_percent INTEGER NOT NULL, pressure_hpa REAL NOT NULL,
 wind_speed_mps REAL NOT NULL, weather_main TEXT NOT NULL,
 weather_description TEXT NOT NULL, source TEXT NOT NULL DEFAULT 'openweathermap',
 FOREIGN KEY(city_id) REFERENCES cities(city_id),
 UNIQUE(city_id, observed_at)
);
CREATE TABLE IF NOT EXISTS pipeline_runs (
 run_id INTEGER PRIMARY KEY AUTOINCREMENT, city_id INTEGER,
 started_at TEXT NOT NULL, completed_at TEXT,
 status TEXT NOT NULL CHECK(status IN ('running','success','failed','skipped')),
 records_processed INTEGER NOT NULL DEFAULT 0, error_message TEXT,
 FOREIGN KEY(city_id) REFERENCES cities(city_id)
);
CREATE INDEX IF NOT EXISTS idx_observations_city_time ON weather_observations(city_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_runs_started_at ON pipeline_runs(started_at);
