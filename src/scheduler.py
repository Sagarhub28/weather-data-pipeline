import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from config import settings
from src.etl_pipeline import run_pipeline
log=logging.getLogger(__name__)

def start_scheduler(cities=None):
    run_pipeline(cities)
    scheduler=BlockingScheduler(timezone="UTC")
    scheduler.add_job(lambda: log.info("Scheduled run: %s",run_pipeline(cities)),
                      "interval",minutes=settings.COLLECTION_INTERVAL_MINUTES,
                      id="weather_etl",max_instances=1,coalesce=True)
    log.info("Scheduler running every %s minutes; Ctrl+C to stop",settings.COLLECTION_INTERVAL_MINUTES)
    try: scheduler.start()
    except (KeyboardInterrupt,SystemExit):
        scheduler.shutdown(wait=False)
        log.info("Scheduler stopped")
