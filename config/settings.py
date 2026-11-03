import os
from pathlib import Path
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "").strip()
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(ROOT / "database/weather_data.db")))
LOG_PATH = Path(os.getenv("LOG_PATH", str(ROOT / "logs/pipeline.log")))
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", str(ROOT / "reports")))
COLLECTION_INTERVAL_MINUTES = max(1, int(os.getenv("COLLECTION_INTERVAL_MINUTES", "60")))
REQUEST_TIMEOUT_SECONDS = max(1, int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10")))
API_MAX_RETRIES = max(1, int(os.getenv("API_MAX_RETRIES", "3")))
HIGH_TEMPERATURE_C = float(os.getenv("HIGH_TEMPERATURE_C", "35"))
HIGH_HUMIDITY_PERCENT = int(os.getenv("HIGH_HUMIDITY_PERCENT", "85"))
DEFAULT_CITIES = ["Mumbai,IN", "Delhi,IN", "Bengaluru,IN", "Chennai,IN", "Kolkata,IN"]
