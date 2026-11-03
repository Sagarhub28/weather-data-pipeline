import logging
from src.api_client import fetch_current_weather
from src.validators import transform_weather
from src.database import connect, setup_database, upsert_city, insert_observation, start_run, finish_run, utc_now
from config import settings
log = logging.getLogger(__name__)

def run_pipeline(cities=None, api_fetcher=None, db_path=None):
    cities, fetcher = cities or settings.DEFAULT_CITIES, api_fetcher or fetch_current_weather
    setup_database(db_path)
    result = {"requested":len(cities),"succeeded":0,"failed":0,"inserted":0,"duplicates":0,"errors":[]}
    for requested in cities:
        started, city_id, run_id = utc_now(), None, None
        try:
            observation = transform_weather(fetcher(requested), fetched_at=utc_now())
            with connect(db_path) as conn:
                city_id = upsert_city(conn, observation["city"])
                run_id = start_run(conn, city_id, started)
                inserted = insert_observation(conn, city_id, observation)
                finish_run(conn, run_id, "success", utc_now(), int(inserted))
            result["succeeded"] += 1
            result["inserted" if inserted else "duplicates"] += 1
            log.info("ETL succeeded for %s; inserted=%s", requested, inserted)
        except Exception as exc:
            result["failed"] += 1
            result["errors"].append({"city":requested,"error":str(exc)})
            log.exception("ETL failed for %s", requested)
            try:
                with connect(db_path) as conn:
                    run_id = start_run(conn, city_id, started)
                    finish_run(conn, run_id, "failed", utc_now(), 0, str(exc)[:1000])
            except Exception:
                log.exception("Could not save failure status")
    return result
