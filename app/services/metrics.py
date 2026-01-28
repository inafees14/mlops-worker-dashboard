from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.event import Event
from datetime import datetime, timedelta
from typing import Optional


def get_summary_metrics(db: Session, hours: Optional[int] = None):
    query = db.query(Event)

    if hours:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Event.timestamp >= cutoff)

    total_events = query.count()
    total_products = query.with_entities(func.sum(Event.count)).scalar() or 0

    active_events = query.filter(Event.event_type == "working").count()
    idle_events = query.filter(Event.event_type == "idle").count()

    last_event_time = query.with_entities(func.max(Event.timestamp)).scalar()

    return {
        "total_events": total_events,
        "total_products": total_products,
        "active_events": active_events,
        "idle_events": idle_events,
        "last_event_time": last_event_time,
    }



def get_worker_metrics(
    db: Session,
    hours: Optional[int] = None,
    worker_id: Optional[str] = None,
):
    query = db.query(Event)

    if hours:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Event.timestamp >= cutoff)

    if worker_id:
        query = query.filter(Event.worker_id == worker_id)

    rows = (
        query.with_entities(
            Event.worker_id,
            func.count(Event.id).label("events"),
            func.sum(Event.count).label("products"),
        )
        .group_by(Event.worker_id)
        .all()
    )

    results = []
    for r in rows:
        productivity_score = (r.products or 0) + (r.events or 0) * 0.1

        results.append({
            "worker_id": r.worker_id,
            "events": r.events,
            "products": r.products or 0,
            "productivity_score": round(productivity_score, 2),
        })

    return results



def get_workstation_metrics(db: Session, hours: Optional[int] = None):
    query = db.query(Event)

    if hours:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Event.timestamp >= cutoff)

    rows = (
        query.with_entities(
            Event.workstation_id,
            func.count(Event.id).label("events"),
            func.sum(Event.count).label("products"),
        )
        .group_by(Event.workstation_id)
        .all()
    )

    return [
        {
            "workstation_id": r.workstation_id,
            "events": r.events,
            "products": r.products or 0,
        }
        for r in rows
    ]

