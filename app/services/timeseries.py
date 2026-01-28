from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.event import Event


from typing import Optional

def get_timeseries(
    db: Session,
    hours: Optional[int] = None,
    worker_id: Optional[str] = None,
):
    query = db.query(
        func.strftime("%Y-%m-%d %H:%M", Event.timestamp).label("minute"),
        func.count(Event.id).label("events"),
        func.sum(Event.count).label("products"),
    )

    if hours:
        since = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Event.timestamp >= since)

    if worker_id:
        query = query.filter(Event.worker_id == worker_id)

    query = query.group_by("minute").order_by("minute")

    rows = query.all()

    return [
        {
            "minute": r.minute,
            "events": int(r.events or 0),
            "products": int(r.products or 0),
        }
        for r in rows
    ]
