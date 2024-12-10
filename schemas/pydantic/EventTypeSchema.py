from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class EventTypeBase(BaseModel):
    """Base schema for event types with common attributes."""

    name: str = Field(
        ..., description="Unique name of the event type"
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the event type",
    )
    event_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="JSON Schema for validating event data",
    )
    icon: Optional[str] = Field(
        None, description="Icon identifier for UI"
    )
    color: Optional[str] = Field(
        None,
        description="Hex color code for UI",
        pattern="^#[0-9a-fA-F]{6}$",
    )

    class Config:
        """Pydantic model configuration."""

        orm_mode = True


class EventTypeCreate(EventTypeBase):
    """Schema for creating a new event type."""

    pass


class EventTypeUpdate(BaseModel):
    """Schema for updating an existing event type."""

    name: Optional[str] = None
    description: Optional[str] = None
    event_schema: Optional[Dict[str, Any]] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(
        None,
        description="Hex color code for UI",
        pattern="^#[0-9a-fA-F]{6}$",
    )

    class Config:
        """Pydantic model configuration."""

        orm_mode = True


class EventTypeResponse(BaseModel):
    """Response schema for event types."""

    id: int
    name: str
    description: Optional[str] = None
    event_schema: Optional[Dict[str, Any]] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(
        None,
        description="Hex color code for UI",
        pattern="^#[0-9a-fA-F]{6}$",
    )

    class Config:
        """Pydantic config."""

        orm_mode = True
