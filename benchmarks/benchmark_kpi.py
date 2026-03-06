import time
import statistics

from app.core.database import SessionLocal
from app.services.metrics import (
    get_summary_metrics,
    get_worker_metrics,
    get_workstation_metrics
)

db = SessionLocal()

runs = []

for i in range(10):

    start = time.perf_counter()

    get_summary_metrics(db)
    get_worker_metrics(db)
    get_workstation_metrics(db)

    end = time.perf_counter()

    t = (end-start)*1000
    runs.append(t)

    print(f"Run {i+1}: {t:.2f} ms")

print("\nAverage KPI time:", statistics.mean(runs))