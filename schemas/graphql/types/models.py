"""GraphQL type definitions for the API."""

from typing import Optional, List, Dict, Any
from datetime import datetime

import strawberry
from strawberry.scalars import JSON

from models.EventTypeModel import (
    EventType as EventTypeModel,
)
from models.LifeEventModel import (
    LifeEvent as LifeEventModel,
)


@strawberry.type
class LifeEvent:
    """GraphQL type for life events."""

    def __init__(
        self,
        id: int,
        timestamp: datetime,
        data: JSON,
        tags: Optional[List[str]] = None,
        location: Optional[str] = None,
        event_type: Optional["EventType"] = None,
    ):
        self._id = id
        self._timestamp = timestamp
        self._data = data
        self._tags = tags
        self._location = location
        self._event_type = event_type

    @strawberry.field(description="Event ID")
    def id(self) -> int:
        return self._id

    @strawberry.field(description="Event timestamp")
    def timestamp(self) -> datetime:
        return self._timestamp

    @strawberry.field(description="Event data")
    def data(self) -> JSON:
        return self._data

    @strawberry.field(description="Event tags")
    def tags(self) -> Optional[List[str]]:
        return self._tags

    @strawberry.field(description="Event location")
    def location(self) -> Optional[str]:
        return self._location

    @strawberry.field(description="Event type")
    def event_type(self) -> Optional["EventType"]:
        return self._event_type

    @classmethod
    def from_db(cls, model: LifeEventModel) -> "LifeEvent":
        """Convert from SQLAlchemy model to GraphQL type."""
        return cls(
            id=model.id,
            timestamp=model.timestamp,
            data=model.data,
            tags=model.tags,
            location=model.location,
            event_type=(
                EventType.from_db(model.event_type)
                if model.event_type
                else None
            ),
        )


@strawberry.type
class EventType:
    """GraphQL type for event types."""

    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        event_schema: Optional[JSON] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None,
        events: Optional[List[LifeEvent]] = None,
    ):
        self._id = id
        self._name = name
        self._description = description
        self._event_schema = event_schema
        self._icon = icon
        self._color = color
        self._events = events

    @strawberry.field(description="Event type ID")
    def id(self) -> int:
        return self._id

    @strawberry.field(description="Event type name")
    def name(self) -> str:
        return self._name

    @strawberry.field(description="Event type description")
    def description(self) -> Optional[str]:
        return self._description

    @strawberry.field(
        description="JSON Schema for validation"
    )
    def event_schema(self) -> Optional[JSON]:
        return self._event_schema

    @strawberry.field(description="Icon identifier")
    def icon(self) -> Optional[str]:
        return self._icon

    @strawberry.field(description="Hex color code")
    def color(self) -> Optional[str]:
        return self._color

    @strawberry.field(description="Associated life events")
    def events(self) -> Optional[List[LifeEvent]]:
        return self._events

    @classmethod
    def from_db(cls, model: EventTypeModel) -> "EventType":
        """Convert from SQLAlchemy model to GraphQL type."""
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            event_schema=model.event_schema,
            icon=model.icon,
            color=model.color,
            events=(
                [
                    LifeEvent.from_db(event)
                    for event in model.events
                ]
                if model.events
                else None
            ),
        )


@strawberry.input
class EventTypeInput:
    """Input type for creating event types."""

    name: str = strawberry.field(
        description="Event type name"
    )

    description: Optional[str] = strawberry.field(
        default=None, description="Optional description"
    )

    event_schema: Optional[JSON] = strawberry.field(
        default=None,
        description="JSON Schema for validation",
    )

    icon: Optional[str] = strawberry.field(
        default=None, description="Icon identifier"
    )

    color: Optional[str] = strawberry.field(
        default=None, description="Hex color code"
    )


@strawberry.input
class EventTypeUpdate:
    """Input type for updating event types."""

    name: Optional[str] = strawberry.field(
        default=None, description="Event type name"
    )

    description: Optional[str] = strawberry.field(
        default=None, description="Optional description"
    )

    event_schema: Optional[JSON] = strawberry.field(
        default=None,
        description="JSON Schema for validation",
    )

    icon: Optional[str] = strawberry.field(
        default=None, description="Icon identifier"
    )

    color: Optional[str] = strawberry.field(
        default=None, description="Hex color code"
    )


@strawberry.input
class LifeEventInput:
    """Input type for creating life events."""

    event_type_id: int = strawberry.field(
        description="Associated event type ID"
    )

    timestamp: datetime = strawberry.field(
        description="Event timestamp"
    )

    data: JSON = strawberry.field(description="Event data")

    tags: Optional[List[str]] = strawberry.field(
        default=None, description="Event tags"
    )

    location: Optional[str] = strawberry.field(
        default=None, description="Event location"
    )


@strawberry.input
class LifeEventUpdate:
    """Input type for updating life events."""

    event_type_id: Optional[int] = strawberry.field(
        default=None,
        description="Associated event type ID",
    )

    timestamp: Optional[datetime] = strawberry.field(
        default=None, description="Event timestamp"
    )

    data: Optional[JSON] = strawberry.field(
        default=None, description="Event data"
    )

    tags: Optional[List[str]] = strawberry.field(
        default=None, description="Event tags"
    )

    location: Optional[str] = strawberry.field(
        default=None, description="Event location"
    )


@strawberry.input
class LifeEventFilter:
    """Input type for filtering life events."""

    event_type_id: Optional[int] = strawberry.field(
        default=None, description="Filter by event type ID"
    )

    start_date: Optional[datetime] = strawberry.field(
        default=None,
        description="Filter events after this date",
    )

    end_date: Optional[datetime] = strawberry.field(
        default=None,
        description="Filter events before this date",
    )

    tags: Optional[List[str]] = strawberry.field(
        default=None, description="Filter by tags"
    )

    limit: int = strawberry.field(
        default=50,
        description="Maximum number of events to return",
    )

    offset: int = strawberry.field(
        default=0, description="Number of events to skip"
    )
