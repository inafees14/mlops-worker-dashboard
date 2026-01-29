from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.services.metrics import (
    get_summary_metrics,
    get_worker_metrics,
    get_workstation_metrics,
)
from app.services.timeseries import get_timeseries
from app.services.analytics import compute_business_metrics

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


@router.get("/summary")
def summary(
    hours: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return get_summary_metrics(db, hours)


@router.get("/workers")
def workers(
    hours: Optional[int] = Query(None),
    worker_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return get_worker_metrics(db, hours, worker_id)


@router.get("/workstations")
def workstations(
    hours: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return get_workstation_metrics(db, hours)


@router.get("/timeseries")
def timeseries(
    hours: Optional[int] = None,
    worker_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_timeseries(db, hours=hours, worker_id=worker_id)

@router.get("/analytics")
def analytics(
    hours: Optional[int] = Query(None),
    worker_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return compute_business_metrics(
        db=db,
        hours=hours,
        worker_id=worker_id,
    )
