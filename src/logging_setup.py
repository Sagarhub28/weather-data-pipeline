import logging
from config import settings
def configure_logging():
    settings.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    for handler in (logging.FileHandler(settings.LOG_PATH, encoding="utf-8"), logging.StreamHandler()):
        handler.setFormatter(fmt)
        root.addHandler(handler)
