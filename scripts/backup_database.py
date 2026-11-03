import argparse
from datetime import datetime
from pathlib import Path
from config import settings
from src.database import connect

def backup(source=None,destination=None):
    source=Path(source or settings.DATABASE_PATH)
    if not source.exists(): raise FileNotFoundError(f"Database not found: {source}")
    destination=Path(destination or source.with_name(f"{source.stem}_backup_{datetime.now():%Y%m%d_%H%M%S}{source.suffix}"))
    destination.parent.mkdir(parents=True,exist_ok=True)
    with connect(source) as src, connect(destination) as dst: src.backup(dst)
    return destination
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--source"); p.add_argument("--destination"); a=p.parse_args()
    print(backup(a.source,a.destination))
