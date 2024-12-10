"""Event type model definition."""

from typing import Optional, List

from sqlalchemy import (
    Integer,
    String,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.schema import Column

from models.BaseModel import Base


class EventType(Base):
    """Model for event types."""

    __tablename__ = "event_types"

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True
    )
    name: Mapped[str] = Column(
        String, unique=True, nullable=False
    )
    description: Mapped[Optional[str]] = Column(
        String, nullable=True
    )
    event_schema: Mapped[Optional[dict]] = Column(
        JSON, nullable=True
    )
    icon: Mapped[Optional[str]] = Column(
        String, nullable=True
    )
    color: Mapped[Optional[str]] = Column(
        String, nullable=True
    )

    # Relationships
    events: Mapped[List["LifeEvent"]] = relationship(
        "LifeEvent",
        back_populates="event_type",
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"<EventType {self.name}>"
