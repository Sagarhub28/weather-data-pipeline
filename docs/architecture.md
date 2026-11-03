
# System Architecture

## 1. Overview

The Weather Data Pipeline System is a Python-based application that collects real-time weather data from the OpenWeatherMap API, validates and processes the data, stores it in a SQLite database, and generates reports and monitoring information.

The system uses a modular architecture in which each component has a specific responsibility.

## 2. Architecture Flow

OpenWeatherMap API
        |
        v
api_client.py
        |
        v
etl_pipeline.py
        |
        v
validators.py
        |
        v
database.py
        |
        v
SQLite Database
        |
        +------> reporter.py
        |          |
        |          v
        |       JSON / CSV Reports
        |
        +------> monitor.py
                   |
                   v
              Health Status

scheduler.py triggers recurring data collection.

## 3. Component Description

### api_client.py
Connects to the OpenWeatherMap API and retrieves current weather information for configured cities.

### etl_pipeline.py
Coordinates the Extract, Transform and Load process. It manages API requests, data processing, validation and database insertion.

### validators.py
Checks required fields, timestamp formats and valid weather measurement ranges before data is stored.

### database.py
Handles SQLite database connections, queries and data insertion.

### scheduler.py
Triggers weather data collection at configured intervals.

### reporter.py
Generates SQL-based historical summaries, weather alerts and JSON/CSV reports.

### monitor.py
Checks database connectivity, data freshness and failed pipeline runs.

## 4. ETL Workflow

1. Extract: Retrieve current weather information from OpenWeatherMap.
2. Transform: Convert API responses into a consistent internal data structure.
3. Validate: Check required fields, timestamps and measurement values.
4. Load: Store validated observations in SQLite.
5. Report: Generate historical summaries and weather reports.

## 5. Error Handling

Each city is processed independently so that a failure for one city does not stop requests for other cities.

API errors and processing failures are logged. Pipeline execution information is stored in the database for monitoring and troubleshooting.

## 6. Database Architecture

The SQLite database contains three main tables:

- cities: Stores city information.
- weather_observations: Stores weather measurements and timestamps.
- pipeline_runs: Stores pipeline execution history, status and errors.

The tables use primary keys, foreign keys and uniqueness constraints to maintain data consistency.

## 7. Reporting and Monitoring

The reporter module generates JSON and CSV reports using stored weather observations.

The monitoring module checks database connectivity, data freshness and failed runs to provide an overview of pipeline health.

## 8. Technology Stack

- Python
- OpenWeatherMap API
- SQLite
- APScheduler
- pytest
- JSON and CSV
