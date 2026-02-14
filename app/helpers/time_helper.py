from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

FILE = Path("dev_time.json") 

def dev_get_extra_minutes():
    if not FILE.exists():
        return 0
    return json.loads(FILE.read_text()).get("minutes", 0)

def dev_add_minutes(minutes: int):
    current = dev_get_extra_minutes()
    FILE.write_text(json.dumps({"minutes": current + minutes}))

def dev_reset_extra_minutes():
    if not FILE.exists():
        with open(FILE, "w") as f:
            f.write("")
    FILE.write_text(json.dumps({"minutes": 0}))

def utcnow() -> datetime:
    dev_extra_time_minutes = dev_get_extra_minutes()
    return datetime.now(timezone.utc) + timedelta(minutes=dev_extra_time_minutes)
