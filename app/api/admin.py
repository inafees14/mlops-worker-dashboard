from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event
from app.services.seeder import seed_database

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.delete("/cleanup")
def cleanup_bad_rows(db: Session = Depends(get_db)):
    deleted = db.query(Event).filter(
        (Event.worker_id == "string") |
        (Event.workstation_id == "string")
    ).delete()
    db.commit()
    return {"deleted_rows": deleted}

@router.delete("/purge")
def purge_dummy_data(db: Session = Depends(get_db)):
    deleted = db.query(Event).filter(Event.source_id == "dummy").delete()
    db.commit()
    return {"deleted_rows": deleted}

@router.post("/seed")
def seed_dummy_data(rows: int = 1000, db: Session = Depends(get_db)):
    seed_database(db, rows=rows)
    return {"status": "ok", "rows": rows}
