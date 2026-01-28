import time
import random
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/events"

WORKERS = ["W1", "W2", "W3", "W4", "W5", "W6"]
STATIONS = ["S1", "S2", "S3", "S4", "S5", "S6"]
EVENT_TYPES = ["working", "idle", "product"]

def generate_event():
    event_type = random.choice(EVENT_TYPES)

    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "worker_id": random.choice(WORKERS),
        "workstation_id": random.choice(STATIONS),
        "event_type": event_type,
        "confidence": round(random.uniform(0.85, 0.99), 2),
        "count": random.randint(1, 3) if event_type == "product" else 0
    }

    return payload


def main():
    print("🚀 Simulator started — sending events...")
    while True:
        try:
            payload = generate_event()
            r = requests.post(API_URL, json=payload, timeout=3)
            print("Sent:", payload, "|", r.json())
        except Exception as e:
            print("❌ Error:", e)

        time.sleep(1.5)   # every ~1.5 sec


if __name__ == "__main__":
    main()


from fastapi import APIRouter
import threading
from app.services.seeder import start_simulator, stop_simulator

router = APIRouter(prefix="/api/simulator", tags=["Simulator"])

@router.post("/start")
def start():
    start_simulator()
    return {"status": "started"}

@router.post("/stop")
def stop():
    stop_simulator()
    return {"status": "stopped"}
