from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional

from app.models.event import Event


def compute_business_metrics(
    db: Session,
    hours: Optional[int] = None,
    worker_id: Optional[str] = None,
):
    query = db.query(Event)

    if hours:
        since = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Event.timestamp >= since)

    if worker_id:
        query = query.filter(Event.worker_id == worker_id)

    total_events = query.count()
    total_units = query.with_entities(func.sum(Event.count)).scalar() or 0

    active_events = query.filter(Event.event_type == "working").count()
    idle_events = query.filter(Event.event_type == "idle").count()

    # ---------------- Business KPIs ----------------

    throughput = round(total_units / max(active_events, 1), 2)
    # Production rate = units per hour (approx)
    production_rate = round(total_units / max((hours or 1), 1), 2)
    idle_ratio = round((idle_events / max(total_events, 1)) * 100, 2)
    yield_rate = round(total_units / max(total_events, 1), 2)
    avg_utilization = round(100 - idle_ratio, 2)

    # ---------------- Operational Metrics ----------------
    # Approximate minutes per event (simulation)
    MINUTES_PER_EVENT = 2
    total_active_minutes = active_events * MINUTES_PER_EVENT
    total_idle_minutes = idle_events * MINUTES_PER_EVENT

    # MTBF / MTTR estimation (simple simulation logic)
    timestamps = (
        query.with_entities(Event.timestamp)
        .order_by(Event.timestamp)
        .all()
    )

    mtbf = 0
    mttr = 0
    if len(timestamps) > 2:
        gaps = []
        for i in range(1, len(timestamps)):
            delta = (timestamps[i][0] - timestamps[i-1][0]).total_seconds()
            gaps.append(delta)

        mtbf = round(sum(gaps) / len(gaps) / 60, 2)  # minutes
        mttr = round(mtbf * 0.3, 2)                  # simulated recovery

    # ---------------- Bottleneck Worker ----------------

    workers = {}
    events = query.all()

    for e in events:
        workers.setdefault(e.worker_id, {"active": 0, "idle": 0})
        if e.event_type == "working":
            workers[e.worker_id]["active"] += 1
        elif e.event_type == "idle":
            workers[e.worker_id]["idle"] += 1

    bottleneck_worker = None
    lowest_util = 100

    for w, stats in workers.items():
        total = stats["active"] + stats["idle"]
        util = (stats["active"] / total * 100) if total else 0
        if util < lowest_util:
            lowest_util = util
            bottleneck_worker = w

    return {
        "throughput_units_per_hour": throughput,
        "production_rate": production_rate,
        "total_active_minutes": total_active_minutes,
        "total_idle_minutes": total_idle_minutes,
        "idle_ratio_percent": idle_ratio,
        "yield_units_per_event": yield_rate,
        "avg_utilization": avg_utilization,
        "bottleneck_worker": bottleneck_worker,

        # Operational KPIs
        "mtbf_minutes": mtbf,
        "mttr_minutes": mttr,
    }
