from sqlalchemy import Column, String
from app.core.database import Base

class Workstation(Base):
    __tablename__ = "mlops_workstations"

    station_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
