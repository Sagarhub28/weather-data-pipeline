# Weather Data Pipeline System

Beginner-friendly multi-city weather ETL project. It extracts current observations from OpenWeatherMap, transforms and validates them, loads them into normalized SQLite tables, and produces historical analytics, alerts, reports, and health checks.

## Setup
1. Install Python 3.10+.
2. Create and activate a virtual environment: `python -m venv .venv`
3. Activate it (`.venv\\Scripts\\activate` on Windows or `source .venv/bin/activate` on macOS/Linux).
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`; add your API key. Never commit `.env`.
6. Run `python -m src.main run`.
7. Run `python -m src.main schedule` to collect every configured interval.

## Commands
- `python -m src.main run --cities "Mumbai,IN" "London,GB"`
- `python -m src.main report --days 30`
- `python -m src.main history --city Mumbai --days 30`
- `python -m src.main stats`
- `python -m src.main health`
- `python -m unittest discover -s tests -v`
- `python scripts/backup_database.py`

Reports go to `reports/`; logs go to `logs/pipeline.log`. Database defaults to `database/weather_data.db`.

## Tables
`cities`, `weather_observations`, `pipeline_runs`. See `docs/database_schema.md` and `docs/architecture.md`.

## Quality and limitations
Validates required fields, ISO timestamps, plausible temperature, humidity bounds, nonnegative pressure/wind, and deduplicates by city/timestamp. API errors are logged and stored in pipeline run history. Current weather is not historical backfill: meaningful 30-day analysis requires regularly scheduled collection or a separate historical dataset. Add screenshots of real local runs under `screenshots/` before submission.
