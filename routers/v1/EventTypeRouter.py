from typing import List, Optional

from fastapi import APIRouter, Depends
from services.EventTypeService import EventTypeService
from schemas.pydantic.EventTypeSchema import (
    EventTypeResponse,
    EventTypeCreate,
    EventTypeUpdate,
)

router = APIRouter(
    prefix="/api/v1/event-types",
    tags=["Event Types"],
)


@router.post("/", response_model=EventTypeResponse)
def create_event_type(
    event_type: EventTypeCreate,
    service: EventTypeService = Depends(),
) -> EventTypeResponse:
    """Create a new event type."""
    db_event_type = service.create(event_type)
    return EventTypeResponse.from_orm(db_event_type)


@router.get("/", response_model=List[EventTypeResponse])
def list_event_types(
    name: Optional[str] = None,
    limit: Optional[int] = 100,
    start: Optional[int] = 0,
    service: EventTypeService = Depends(),
) -> List[EventTypeResponse]:
    """List all event types."""
    db_event_types = service.list(
        name=name,
        limit=limit,
        start=start,
    )
    return [
        EventTypeResponse.from_orm(event_type)
        for event_type in db_event_types
    ]


@router.get(
    "/{event_type_id}", response_model=EventTypeResponse
)
def get_event_type(
    event_type_id: int,
    service: EventTypeService = Depends(),
) -> EventTypeResponse:
    """Get a specific event type."""
    db_event_type = service.get(event_type_id)
    return EventTypeResponse.from_orm(db_event_type)


@router.put(
    "/{event_type_id}", response_model=EventTypeResponse
)
def update_event_type(
    event_type_id: int,
    event_type: EventTypeUpdate,
    service: EventTypeService = Depends(),
) -> EventTypeResponse:
    """Update an event type."""
    db_event_type = service.update(
        event_type_id, event_type
    )
    return EventTypeResponse.from_orm(db_event_type)


@router.delete("/{event_type_id}")
def delete_event_type(
    event_type_id: int,
    service: EventTypeService = Depends(),
) -> None:
    """Delete an event type."""
    return service.delete(event_type_id)
