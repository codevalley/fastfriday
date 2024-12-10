from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql.schema import Column

from models.BaseModel import Base


class LifeEvent(Base):
    """Model for life events."""

    __tablename__ = "life_events"

    id: Mapped[int] = Column(
        Integer, primary_key=True, index=True
    )
    timestamp: Mapped[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    event_type_id: Mapped[int] = Column(
        Integer,
        ForeignKey("event_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    data: Mapped[dict] = Column(JSON, nullable=False)

    # Relationships
    event_type = relationship(
        "EventType", back_populates="events"
    )

    def __repr__(self) -> str:
        return f"<LifeEvent {self.event_type_id}:{self.timestamp}>"

    @property
    def event_name(self) -> Optional[str]:
        """Get the name of the associated event type."""
        return (
            self.event_type.name
            if self.event_type
            else None
        )
