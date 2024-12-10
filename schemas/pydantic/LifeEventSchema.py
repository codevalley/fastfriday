from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field


class LifeEventBase(BaseModel):
    """Base schema for life events with common attributes."""

    timestamp: datetime = Field(
        default_factory=datetime.now
    )
    data: Dict[str, Any] = Field(
        ...,
        description="Event-specific data following the event type schema",
    )

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
        arbitrary_types_allowed = True


class LifeEventCreate(LifeEventBase):
    """Schema for creating a new life event."""

    event_type_id: int = Field(
        ..., description="ID of the associated event type"
    )

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
        arbitrary_types_allowed = True


class LifeEventUpdate(BaseModel):
    """Schema for updating an existing life event."""

    timestamp: datetime | None = None
    data: Dict[str, Any] | None = None

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
        arbitrary_types_allowed = True


class LifeEventResponse(LifeEventBase):
    """Schema for life event responses including database fields."""

    id: int
    event_type_id: int
    event_name: str

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
        arbitrary_types_allowed = True
