from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib

from app.core.database import get_db
from app.models.event import Event
from app.api.schemas import EventIn

router = APIRouter(prefix="/api", tags=["Events"])


@router.post("/events")
def ingest_event(payload: EventIn, db: Session = Depends(get_db)):
    raw = f"{payload.timestamp}{payload.worker_id}{payload.workstation_id}{payload.event_type}{payload.count}"
    event_hash = hashlib.sha256(raw.encode()).hexdigest()

    existing = db.query(Event).filter(Event.event_hash == event_hash).first()
    if existing:
        return {"status": "duplicate_event_ignored"}
    if payload.worker_id.lower() == "string" or payload.workstation_id.lower() == "string":
        return {"status": "invalid_payload_ignored"}
    event = Event(
        timestamp=payload.timestamp,
        worker_id=payload.worker_id,
        workstation_id=payload.workstation_id,
        event_type=payload.event_type,
        confidence=payload.confidence,
        count=payload.count or 0,
        event_hash=event_hash,
    )

    db.add(event)
    db.commit()

    return {"status": "event_ingested"}
