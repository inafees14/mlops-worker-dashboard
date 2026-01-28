from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventIn(BaseModel):
    timestamp: datetime
    worker_id: str
    workstation_id: str
    event_type: str
    confidence: float
    count: Optional[int] = 0
