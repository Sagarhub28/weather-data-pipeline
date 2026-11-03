import argparse, json
from src.logging_setup import configure_logging
from src.database import setup_database
from src.etl_pipeline import run_pipeline
from src.reporter import generate_report, historical_summary
from src.monitor import health_check

def main():
    p=argparse.ArgumentParser(description="Weather Data Pipeline")
    sub=p.add_subparsers(dest="cmd",required=True)
    r=sub.add_parser("run"); r.add_argument("--cities",nargs="+")
    sub.add_parser("schedule")
    rep=sub.add_parser("report"); rep.add_argument("--days",type=int,default=30)
    sub.add_parser("stats")
    h=sub.add_parser("health"); h.add_argument("--stale-after-hours",type=int,default=3)
    hist=sub.add_parser("history"); hist.add_argument("--city"); hist.add_argument("--days",type=int,default=30)
    a=p.parse_args(); configure_logging(); setup_database()
    if a.cmd=="run":
        result=run_pipeline(a.cities); print(json.dumps(result,indent=2))
        raise SystemExit(1 if result["failed"] else 0)
    if a.cmd=="schedule":
        from src.scheduler import start_scheduler
        start_scheduler()
    elif a.cmd=="report": print(json.dumps(generate_report(days=a.days),indent=2))
    elif a.cmd=="stats": print(json.dumps(health_check(),indent=2))
    elif a.cmd=="health":
        result=health_check(stale_after_hours=a.stale_after_hours); print(json.dumps(result,indent=2))
        raise SystemExit(1 if result["status"]!="healthy" else 0)
    elif a.cmd=="history": print(json.dumps(historical_summary(a.days,a.city),indent=2))
if __name__=="__main__": main()
