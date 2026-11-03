import csv, json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from config import settings
from src.database import connect, setup_database

def latest_observations(db_path=None):
    setup_database(db_path)
    sql = """SELECT c.city_name,c.country_code,w.observed_at,w.temperature_c,w.humidity_percent,
             w.pressure_hpa,w.wind_speed_mps,w.weather_main,w.weather_description
             FROM weather_observations w JOIN cities c ON c.city_id=w.city_id
             JOIN (SELECT city_id,MAX(observed_at) latest FROM weather_observations GROUP BY city_id) x
             ON x.city_id=w.city_id AND x.latest=w.observed_at ORDER BY c.city_name"""
    with connect(db_path) as conn:
        return [dict(r) for r in conn.execute(sql)]

def historical_summary(days=30, city=None, db_path=None):
    setup_database(db_path)
    cutoff = (datetime.now(timezone.utc)-timedelta(days=max(1,days))).isoformat(timespec="seconds").replace("+00:00","Z")
    sql = """SELECT c.city_name,c.country_code,COUNT(*) observations,
             ROUND(AVG(w.temperature_c),2) avg_temperature_c,
             ROUND(MIN(w.temperature_c),2) min_temperature_c,
             ROUND(MAX(w.temperature_c),2) max_temperature_c,
             ROUND(AVG(w.humidity_percent),2) avg_humidity_percent,
             ROUND(AVG(w.wind_speed_mps),2) avg_wind_speed_mps
             FROM weather_observations w JOIN cities c ON c.city_id=w.city_id
             WHERE w.observed_at >= ?"""
    params = [cutoff]
    if city:
        sql += " AND LOWER(c.city_name)=LOWER(?)"; params.append(city)
    sql += " GROUP BY c.city_id ORDER BY avg_temperature_c DESC"
    with connect(db_path) as conn: return [dict(r) for r in conn.execute(sql,params)]

def build_alerts(rows):
    alerts = []
    for r in rows:
        if r["temperature_c"] > settings.HIGH_TEMPERATURE_C:
            alerts.append({"type":"high_temperature","city":r["city_name"],"value":r["temperature_c"],
                           "message":f'{r["city_name"]}: {r["temperature_c"]} C exceeds threshold'})
        if r["humidity_percent"] > settings.HIGH_HUMIDITY_PERCENT:
            alerts.append({"type":"high_humidity","city":r["city_name"],"value":r["humidity_percent"],
                           "message":f'{r["city_name"]}: humidity exceeds threshold'})
    return alerts

def generate_report(db_path=None, reports_dir=None, days=30):
    latest, summary = latest_observations(db_path), historical_summary(days, db_path=db_path)
    with connect(db_path) as conn:
        stats = {"cities_tracked":conn.execute("SELECT COUNT(*) FROM cities").fetchone()[0],
                 "total_observations":conn.execute("SELECT COUNT(*) FROM weather_observations").fetchone()[0],
                 "pipeline_runs":conn.execute("SELECT COUNT(*) FROM pipeline_runs").fetchone()[0],
                 "failed_runs":conn.execute("SELECT COUNT(*) FROM pipeline_runs WHERE status='failed'").fetchone()[0]}
    report = {"generated_at":datetime.now(timezone.utc).isoformat(),"period_days":days,
              "statistics":stats,"latest_weather":latest,"historical_summary":summary,"alerts":build_alerts(latest)}
    out = Path(reports_dir or settings.REPORTS_DIR); out.mkdir(parents=True,exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    jp, cp = out/f"weather_report_{stamp}.json", out/f"weather_summary_{stamp}.csv"
    jp.write_text(json.dumps(report,indent=2),encoding="utf-8")
    cols = ["city_name","country_code","observations","avg_temperature_c","min_temperature_c",
            "max_temperature_c","avg_humidity_percent","avg_wind_speed_mps"]
    with cp.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols); writer.writeheader(); writer.writerows(summary)
    report["files"]={"json":str(jp),"csv":str(cp)}
    return report
