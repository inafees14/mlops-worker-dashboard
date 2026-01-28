from sqlalchemy import Column, String
from app.core.database import Base

class Worker(Base):
    __tablename__ = "mlops_workers"

    worker_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)