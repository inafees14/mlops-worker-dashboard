from sqlalchemy.orm import Session
from sqlalchemy import func, text
from datetime import datetime, timedelta
from typing import Optional

from app.models.event import Event


def get_timeseries(
    db: Session,
    hours: Optional[int] = None,
    worker_id: Optional[str] = None,
):
    query = db.query(Event)

    # ---------------- Filters ----------------
    if hours:
        since = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Event.timestamp >= since)

    if worker_id:
        query = query.filter(Event.worker_id == worker_id)

    # ---------------- Database Compatibility ----------------
    engine_name = db.bind.dialect.name.lower()

    # SQLite → strftime
    if "sqlite" in engine_name:
        time_bucket = func.strftime(
            "%Y-%m-%d %H:%M", Event.timestamp
        ).label("minute")

    # Postgres → date_trunc
    else:
        time_bucket = func.date_trunc(
            "minute", Event.timestamp
        ).label("minute")

    # ---------------- Aggregation ----------------
    rows = (
        db.query(
            time_bucket,
            func.count(Event.id).label("events"),
            func.coalesce(func.sum(Event.count), 0).label("products"),
        )
        .group_by(time_bucket)
        .order_by(time_bucket)
        .all()
    )

    # ---------------- Response Formatting ----------------
    result = []
    for r in rows:
        result.append({
            "minute": str(r.minute),
            "events": int(r.events),
            "products": int(r.products),
        })

    return result
