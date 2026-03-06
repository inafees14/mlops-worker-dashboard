import time
import statistics

from app.core.database import SessionLocal
from app.services.metrics import (
    get_summary_metrics,
    get_worker_metrics,
    get_workstation_metrics
)

db = SessionLocal()

summary_runs = []
worker_runs = []
station_runs = []

for i in range(10):

    start=time.perf_counter()
    get_summary_metrics(db)
    summary_runs.append((time.perf_counter()-start)*1000)

    start=time.perf_counter()
    get_worker_metrics(db)
    worker_runs.append((time.perf_counter()-start)*1000)

    start=time.perf_counter()
    get_workstation_metrics(db)
    station_runs.append((time.perf_counter()-start)*1000)

print("Summary avg:", statistics.mean(summary_runs))
print("Worker avg:", statistics.mean(worker_runs))
print("Station avg:", statistics.mean(station_runs))