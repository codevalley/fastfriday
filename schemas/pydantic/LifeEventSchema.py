from datetime import datetime
from typing import Dict, Any, Optional
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

    timestamp: Optional[datetime] = None
    data: Optional[Dict[str, Any]] = None
    event_type_id: Optional[int] = Field(
        None, description="ID of the associated event type"
    )

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
        arbitrary_types_allowed = True


class LifeEventResponse(BaseModel):
    """Response schema for life events."""

    id: int
    timestamp: datetime
    event_type_id: int
    data: Dict[str, Any]

    class Config:
        """Pydantic config."""

        orm_mode = True
