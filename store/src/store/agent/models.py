from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from database.core import Base


class ProcessedAgent(Base):
    __tablename__ = "processed_agent"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    road_state: Mapped[str] = mapped_column(String(255), nullable=False)
    x: Mapped[float] = mapped_column(nullable=False)
    y: Mapped[float] = mapped_column(nullable=False)
    z: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
