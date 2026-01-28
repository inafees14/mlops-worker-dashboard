from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.seeder import seed_database

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/seed")
def seed(db: Session = Depends(get_db)):
    seed_database(db)
    return {"status": "database seeded successfully"}
