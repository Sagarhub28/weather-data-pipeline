from datetime import datetime, timezone

class DataValidationError(ValueError):
    pass

def transform_weather(data, fetched_at=None):
    try:
        main, weather = data["main"], data["weather"][0]
        sys_data, coord, wind = data.get("sys",{}), data.get("coord",{}), data.get("wind",{})
        observed = datetime.fromtimestamp(int(data["dt"]), timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
        result = {
          "city":{"city_name":str(data["name"]).strip(),"country_code":str(sys_data.get("country","")).strip(),
                  "latitude":coord.get("lat"),"longitude":coord.get("lon")},
          "observed_at":observed,
          "fetched_at":fetched_at or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z"),
          "temperature_c":float(main["temp"]),
          "feels_like_c":float(main["feels_like"]) if main.get("feels_like") is not None else None,
          "humidity_percent":int(main["humidity"]), "pressure_hpa":float(main["pressure"]),
          "wind_speed_mps":float(wind.get("speed",0)), "weather_main":str(weather["main"]).strip(),
          "weather_description":str(weather["description"]).strip(),"source":"openweathermap"}
    except (KeyError, IndexError, TypeError, ValueError, OverflowError) as exc:
        raise DataValidationError(f"Malformed API response: {exc}") from exc
    validate_observation(result)
    return result

def validate_observation(o):
    required = ["observed_at","fetched_at","temperature_c","humidity_percent","pressure_hpa",
                "wind_speed_mps","weather_main","weather_description"]
    missing = [k for k in required if o.get(k) is None or o.get(k) == ""]
    if missing: raise DataValidationError("Missing fields: " + ", ".join(missing))
    try:
        datetime.fromisoformat(o["observed_at"].replace("Z","+00:00"))
        datetime.fromisoformat(o["fetched_at"].replace("Z","+00:00"))
    except (ValueError, TypeError) as exc:
        raise DataValidationError("Invalid ISO-8601 timestamp") from exc
    if not -100 <= float(o["temperature_c"]) <= 70: raise DataValidationError("Temperature out of bounds")
    if not 0 <= int(o["humidity_percent"]) <= 100: raise DataValidationError("Humidity must be 0..100")
    if float(o["pressure_hpa"]) < 0: raise DataValidationError("Pressure cannot be negative")
    if float(o["wind_speed_mps"]) < 0: raise DataValidationError("Wind speed cannot be negative")
    if not o.get("city",{}).get("city_name"): raise DataValidationError("City name is required")
    return True
