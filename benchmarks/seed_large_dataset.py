import random
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(".."))

from app.core.database import SessionLocal, Base, engine
from app.models.event import Event

Base.metadata.create_all(bind=engine)

db = SessionLocal()

workers = ["W1","W2","W3","W4","W5"]
stations = ["S1","S2","S3","S4"]

db.query(Event).delete()
db.commit()

def seed(n=100000):
    base_time = datetime.utcnow()

    for i in range(n):
        event = Event(
            timestamp=base_time + timedelta(seconds=i),
            worker_id=random.choice(workers),
            workstation_id=random.choice(stations),
            event_type=random.choice(["working","idle"]),
            count=random.randint(1,5),
            confidence=random.uniform(0.7,0.99),
            event_hash=f"bench_hash_{i}_{random.randint(1,999999)}"
        )
        db.add(event)

    db.commit()
    print(f"{n} events inserted.")

if __name__ == "__main__":
    seed(100000)