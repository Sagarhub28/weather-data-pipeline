import logging, time, requests
from config import settings
log = logging.getLogger(__name__)
URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherAPIError(RuntimeError):
    pass

def fetch_current_weather(city, api_key=None, session=None):
    key = api_key if api_key is not None else settings.API_KEY
    if not key or key == "replace_me":
        raise WeatherAPIError("Set OPENWEATHERMAP_API_KEY in your .env file.")
    client = session or requests
    last = None
    for attempt in range(1, settings.API_MAX_RETRIES + 1):
        try:
            response = client.get(URL, params={"q":city,"appid":key,"units":"metric"},
                                  timeout=settings.REQUEST_TIMEOUT_SECONDS)
            if response.status_code != 429 and 400 <= response.status_code < 500:
                response.raise_for_status()
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise WeatherAPIError("Unexpected API response format.")
            return payload
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status and 400 <= status < 500 and status != 429:
                raise WeatherAPIError(f"API rejected {city} (HTTP {status}); check key/city.") from exc
            last = exc
        except requests.exceptions.RequestException as exc:
            last = exc
        if attempt < settings.API_MAX_RETRIES:
            delay = min(2 ** (attempt - 1), 8)
            log.warning("Request failed for %s; retrying in %ss", city, delay)
            time.sleep(delay)
    raise WeatherAPIError(f"Unable to fetch {city} after retries: {last}") from last
