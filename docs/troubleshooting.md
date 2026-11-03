
# Troubleshooting Guide

## 1. Missing API Key

**Problem:** The application cannot authenticate with OpenWeatherMap.

**Solution:**
1. Copy `.env.example` to `.env`.
2. Open `.env`.
3. Set the API key using the variable name expected by `src/api_client.py`.
4. Save the file and run the pipeline again.

Never upload `.env` to GitHub.

## 2. HTTP 401 or 403 Errors

**Problem:** The API rejects the request.

**Possible causes:**
- Invalid API key.
- API key has not finished activating.
- API access or account restrictions.

**Solution:** Verify the API key and check your OpenWeatherMap account.

## 3. HTTP 404 Error

**Problem:** The requested city cannot be found.

**Solution:** Include the country code in the city query.

Example: `Mumbai,IN`

## 4. Missing Python Dependencies

**Problem:** Python reports `ModuleNotFoundError`.

**Solution:**

Activate the virtual environment and install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If a specific dependency is missing, verify that it is listed in `requirements.txt`.

## 5. Scheduler Not Running

**Problem:** Scheduled weather collection does not start.

**Possible causes:**
- Required scheduler dependency is not installed.
- Scheduler configuration is incorrect.
- The application process has stopped.

**Solution:**
1. Install project dependencies.
2. Run `python -m src.main schedule`.
3. Keep the terminal open while the scheduler runs.
4. Stop the scheduler with `Ctrl + C`.

## 6. No 30-Day Historical Data

**Problem:** Historical reports do not contain a full 30 days of observations.

**Explanation:** The OpenWeatherMap current-weather endpoint does not automatically backfill historical observations.

**Solution:** Run the pipeline regularly using the scheduler so observations accumulate over time.

## 7. SQLite Database Locked

**Problem:** SQLite reports that the database is locked.

**Solution:**
- Close other applications or processes writing to the database.
- Avoid running multiple schedulers simultaneously.
- Retry the operation after the database is available.

## 8. Report Generation Problems

**Problem:** JSON or CSV reports are missing.

**Solution:**
1. Run `python -m src.main run` to collect weather data.
2. Run `python -m src.main report`.
3. Check the `reports/` directory.
4. Check `logs/pipeline.log` for errors.

## 9. Running Automated Tests

Run the test suite using:

```powershell
python -m pytest -q
```

A successful test run displays the number of passed tests.

## 10. Checking Pipeline Health

Run:

```powershell
python -m src.main health
```

Check the database status, number of tracked cities, observation count, failed runs, and data freshness.

## 11. Useful Project Commands

| Purpose | Command |
|---|---|
| Collect weather data | `python -m src.main run` |
| Generate reports | `python -m src.main report` |
| View statistics | `python -m src.main stats` |
| Check health | `python -m src.main health` |
| View history | `python -m src.main history --city Mumbai --days 30` |
| Start scheduler | `python -m src.main schedule` |
| Run tests | `python -m pytest -q` |
