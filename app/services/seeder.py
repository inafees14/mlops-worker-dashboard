from datetime import datetime, timedelta
import random
import hashlib

from sqlalchemy.orm import Session
from app.models.worker import Worker
from app.models.workstation import Workstation
from app.models.event import Event


WORKERS = [
    ("W1", "Amit"),
    ("W2", "Rahul"),
    ("W3", "Sneha"),
    ("W4", "Priya"),
    ("W5", "Vikram"),
    ("W6", "Neha"),
]

STATIONS = [
    ("S1", "Assembly"),
    ("S2", "Packing"),
    ("S3", "Quality"),
    ("S4", "Welding"),
    ("S5", "Painting"),
    ("S6", "Logistics"),
]

EVENT_TYPES = ["working", "idle", "product_count"]


def seed_database(db: Session, rows: int = 300):
    # Clear old data
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()
    db.commit()

    # Insert workers
    for wid, name in WORKERS:
        db.add(Worker(worker_id=wid, name=name))

    # Insert stations
    for sid, name in STATIONS:
        db.add(Workstation(station_id=sid, name=name))

    db.commit()

    base_time = datetime.utcnow() - timedelta(hours=4)

    for _ in range(rows):
        ts = base_time + timedelta(minutes=random.randint(0, 240))
        worker_id, _ = random.choice(WORKERS)
        station_id, _ = random.choice(STATIONS)
        event_type = random.choice(EVENT_TYPES)

        count = 0
        if event_type == "product_count":
            count = random.randint(1, 5)

        salt = random.random()
        raw = f"{ts}{worker_id}{station_id}{event_type}{count}{salt}"
        event_hash = hashlib.sha256(raw.encode()).hexdigest()

        event = Event(
            timestamp=ts,
            worker_id=worker_id,
            workstation_id=station_id,
            event_type=event_type,
            confidence=round(random.uniform(0.8, 0.99), 2),
            count=count,
            event_hash=event_hash,
            source_id="dummy",   # important
        )

        db.add(event)

    db.commit()


from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.event import Event

def seed_if_empty():
    db: Session = SessionLocal()
    try:
        count = db.query(Event).count()
        if count == 0:
            print("Database empty — auto seeding...")
            seed_dummy_data(db, rows=200)   # keep reasonable
        else:
            print("Database already seeded.")
    except Exception as e:
        print("Seed skipped:", e)
    finally:
        db.close()

