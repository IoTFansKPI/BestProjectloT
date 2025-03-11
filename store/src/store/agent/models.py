from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from database.core import Base


class ProcessedAgent(Base):
    __tablename__ = "processed_agent"
    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    road_state: MappedColumn[str] = mapped_column(String(255), nullable=False)
    x: MappedColumn[float]
    y: MappedColumn[float]
    z: MappedColumn[float]
    latitude: MappedColumn[float]
    longitude: MappedColumn[float]
    timestamp: MappedColumn[datetime]
