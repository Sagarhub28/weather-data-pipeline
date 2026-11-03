from datetime import datetime, timezone
from src.database import connect, setup_database

def health_check(db_path=None, stale_after_hours=3):
    setup_database(db_path)
    with connect(db_path) as conn:
        conn.execute("SELECT 1")
        cities=conn.execute("SELECT COUNT(*) FROM cities").fetchone()[0]
        observations=conn.execute("SELECT COUNT(*) FROM weather_observations").fetchone()[0]
        latest=conn.execute("SELECT MAX(observed_at) FROM weather_observations").fetchone()[0]
        last_run=conn.execute("SELECT MAX(completed_at) FROM pipeline_runs").fetchone()[0]
        failed=conn.execute("SELECT COUNT(*) FROM pipeline_runs WHERE status='failed'").fetchone()[0]
    stale=True
    if latest:
        try:
            dt=datetime.fromisoformat(latest.replace("Z","+00:00"))
            stale=(datetime.now(timezone.utc)-dt).total_seconds()>stale_after_hours*3600
        except ValueError: pass
    return {"database":"ok","cities_tracked":cities,"observations":observations,
            "latest_observation":latest,"last_completed_run":last_run,"failed_runs":failed,
            "data_stale":stale,"status":"degraded" if stale or failed else "healthy"}
