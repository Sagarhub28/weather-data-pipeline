
# Weather Data Pipeline System

A Python-based, multi-city weather data pipeline that collects real-time weather observations from OpenWeatherMap, validates and transforms the data, stores it in SQLite, and generates historical summaries, alerts, reports, and health checks.

## 1. Project Objectives

- Collect current weather observations from OpenWeatherMap.
- Validate and transform API responses before database insertion.
- Store city information, weather observations, and pipeline execution history in SQLite.
- Analyze accumulated weather data and generate reports.
- Generate threshold-based weather alerts.
- Monitor pipeline health and record failures for troubleshooting.

## 2. Technology Stack

- Python 3.10+
- OpenWeatherMap Current Weather API
- SQLite
- APScheduler
- pytest
- JSON and CSV

## 3. Project Setup

### Prerequisites

Install Python 3.10 or later.

### Installation

1. Open a terminal in the project directory.
2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate it on Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`.
6. Add your OpenWeatherMap API key using the variable name expected by `src/api_client.py`.
7. Run the pipeline:

   ```powershell
   python -m src.main run
   ```

Never upload your actual `.env` file or API key to GitHub.

## 4. Available Commands

Run commands from the project root directory.

| Purpose | Command |
|---|---|
| Collect weather data | `python -m src.main run` |
| Collect selected cities | `python -m src.main run --cities "Mumbai,IN" "London,GB"` |
| Generate reports | `python -m src.main report --days 30` |
| View city history | `python -m src.main history --city Mumbai --days 30` |
| View statistics | `python -m src.main stats` |
| Check pipeline health | `python -m src.main health` |
| Start scheduler | `python -m src.main schedule` |
| Run automated tests | `python -m pytest -q` |
| Back up database | `python scripts/backup_database.py` |

The scheduler runs in the foreground. Keep its terminal open while it is running.

## 5. System Architecture and ETL Workflow

The application follows an Extract, Transform, Load (ETL) architecture.

1. **Extract:** `api_client.py` retrieves current weather information from OpenWeatherMap.
2. **Transform:** `etl_pipeline.py` processes API responses into a consistent structure.
3. **Validate:** `validators.py` checks required fields, timestamps, and measurement ranges.
4. **Load:** `database.py` stores validated observations in SQLite.
5. **Analyze:** Historical queries calculate summary statistics from stored observations.
6. **Report:** `reporter.py` generates JSON and CSV reports and evaluates weather alert thresholds.
7. **Monitor:** `monitor.py` checks database connectivity, data freshness, and failed pipeline runs.
8. **Schedule:** `scheduler.py` triggers recurring weather collection.

See `docs/architecture.md` for the architecture overview.

## 6. Database Design

The SQLite database contains three main tables:

- `cities`: Stores city names, country codes, and geographic coordinates.
- `weather_observations`: Stores time-stamped weather measurements.
- `pipeline_runs`: Stores execution status, processing counts, and error details.

Primary keys, foreign keys, unique constraints, and indexes help maintain data consistency.

Database location: `database/weather_data.db`

See `database/schema.sql` and `docs/database_schema.md` for details.

## 7. Technical Requirements Mapping

| Requirement | Implementation |
|---|---|
| SQLite with at least three related tables | `database/schema.sql` |
| OpenWeatherMap API integration | `src/api_client.py` |
| ETL pipeline and error handling | `src/etl_pipeline.py` |
| Data validation | `src/validators.py` |
| Automated scheduling | `src/scheduler.py` |
| Historical analysis | `src/main.py`, `src/reporter.py` |
| Reports and weather alerts | `src/reporter.py` |
| Health checks and monitoring | `src/monitor.py` |
| Automated tests | `tests/` |
| Database backup | `scripts/backup_database.py` |
| Documentation | `docs/` |

## 8. Reports, Logs, and Monitoring

Generated reports are saved in:

`reports/`

Pipeline logs are saved in:

`logs/pipeline.log`

The health command:

```powershell
python -m src.main health
```

provides information about database connectivity, tracked cities, observation counts, failed runs, and data freshness.

## 9. Testing

Run the automated test suite:

```powershell
python -m pytest -q
```

The last verified test result was **5 passed**. Run the tests again before submission to verify the final project version.

## 10. Documentation

Additional project documentation is available in `docs/`:

- `architecture.md` – System architecture and ETL workflow.
- `api_guide.md` – API endpoint, parameters, and error handling.
- `database_schema.md` – Database tables and relationships.
- `troubleshooting.md` – Common problems and solutions.

## 11. Screenshots

Add genuine screenshots from your local project to the `screenshots/` directory.

Recommended screenshots:

- `pipeline_run.png` – Successful weather data extraction and loading.
- `test_results.png` – Automated test results.
- `health_check.png` – Database and pipeline health status.
- `generated_reports.png` – Generated reports and weather alerts.

Only include screenshots that actually exist and show real project output.

## 12. Deployment and Security

1. Install Python and project dependencies.
2. Configure the API key in the local `.env` file.
3. Initialize and verify the SQLite database.
4. Run the pipeline and automated tests.
5. Verify scheduler operation before relying on automated collection.
6. Keep API keys, virtual environments, and local secrets out of the GitHub repository.

Use `.env.example` with placeholder values for sharing configuration instructions.

## 13. Known Limitations

- The current-weather API endpoint does not automatically backfill historical weather data.
- Historical analysis depends on observations accumulated over time or a separate historical dataset.
- A complete 30-day analysis requires sufficient stored observations.
- The scheduler must be running for regular automated collection.
- Weather alerts depend on the thresholds configured in the application.
