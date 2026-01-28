from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "mlops_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    worker_id = Column(String)
    workstation_id = Column(String)
    event_type = Column(String)
    confidence = Column(Float)
    count = Column(Integer, default=0)
    event_hash = Column(String, unique=True)
    source_id = Column(String, default="camera-1")
    created_at = Column(DateTime, default=datetime.utcnow)
