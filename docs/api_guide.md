# API Integration Guide

## 1. API Overview

The Weather Data Pipeline System uses the OpenWeatherMap Current Weather API to retrieve real-time weather observations for configured cities.

## 2. API Endpoint

GET https://api.openweathermap.org/data/2.5/weather

## 3. Request Parameters

| Parameter | Description | Example |
|---|---|---|
| q | City name and country code | Mumbai,IN |
| appid | OpenWeatherMap API key | Stored in .env |
| units | Measurement system | metric |

The metric unit system returns temperature in Celsius and wind speed in metres per second.

## 4. API Authentication

The API key is stored in the project's `.env` file.

Example configuration:

OPENWEATHER_API_KEY=your_api_key_here

The actual API key must not be committed to GitHub or included in project screenshots.

## 5. API Response

The API returns weather information in JSON format.

The response can include:
- City name and location information
- Temperature and feels-like temperature
- Humidity
- Atmospheric pressure
- Wind speed
- Main weather condition and description
- Observation timestamp

The pipeline extracts the required fields and transforms them into a consistent format before database insertion.

## 6. Error Handling

The API client uses HTTP timeouts and bounded retries.

- Temporary request failures may be retried.
- Most HTTP 4xx errors are surfaced without retries.
- API and processing errors are logged.
- A failure for one city does not stop processing other configured cities.

## 7. Data Limitations

The endpoint provides current weather observations, not a complete historical weather archive.

Historical analysis depends on observations collected and stored by the pipeline over time.

Example cities and values in project documentation are illustrative and should not be treated as live API results.