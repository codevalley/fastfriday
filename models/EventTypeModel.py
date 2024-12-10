from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from models.BaseModel import EntityMeta


class EventType(EntityMeta):
    """
    EventType represents a category of life events with its associated metadata and validation schema.
    Examples: Photo, Meal, Exercise, Sleep, Work, etc.
    """

    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200), nullable=True)
    schema = Column(
        JSON, nullable=True
    )  # JSON Schema for validating event data
    icon = Column(
        String(50), nullable=True
    )  # Icon identifier for UI
    color = Column(
        String(7), nullable=True
    )  # Hex color code

    # Relationships
    events = relationship(
        "LifeEvent",
        back_populates="event_type",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<EventType {self.name}>"
