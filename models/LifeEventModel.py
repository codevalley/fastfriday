from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import relationship

from models.BaseModel import Base


class LifeEvent(Base):
    """
    LifeEvent represents a single event in a person's life.
    The event's specific data is stored in the JSON 'data' field,
    structured according to the associated event_type's schema.
    """

    __tablename__ = "life_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    data = Column(JSON, nullable=False)

    # Foreign Keys
    event_type_id = Column(
        Integer,
        ForeignKey("event_types.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Relationships
    event_type = relationship(
        "EventType", back_populates="events"
    )

    def __repr__(self):
        return f"<LifeEvent {self.event_type_id}:{self.timestamp}>"

    @property
    def event_name(self):
        """Get the name of the associated event type"""
        return (
            self.event_type.name
            if self.event_type
            else None
        )
