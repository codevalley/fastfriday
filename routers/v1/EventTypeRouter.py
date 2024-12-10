from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.EventTypeModel import EventType  # noqa: F401
from schemas.pydantic.EventTypeSchema import (
    EventTypeCreate,
    EventTypeResponse,
    EventTypeUpdate,
)
from services.EventTypeService import EventTypeService
from configs.database import get_db

router = APIRouter(
    prefix="/api/v1/event-types",
    tags=["event-types"],
    responses={404: {"description": "Not found"}},
)


def get_service() -> EventTypeService:
    """Get service instance."""
    return EventTypeService()


@router.post("/", response_model=EventTypeResponse)
def create_event_type(
    event_type: EventTypeCreate,
    service: EventTypeService = Depends(get_service),
    db: Session = Depends(get_db),
) -> EventTypeResponse:
    """Create a new event type."""
    return service.create_event_type(event_type, db)


@router.get("/", response_model=List[EventTypeResponse])
def list_event_types(
    skip: int = 0,
    limit: int = 100,
    service: EventTypeService = Depends(get_service),
    db: Session = Depends(get_db),
) -> List[EventTypeResponse]:
    """List all event types."""
    return service.get_event_types(skip, limit, db)


@router.get("/{type_id}", response_model=EventTypeResponse)
def get_event_type(
    type_id: int,
    service: EventTypeService = Depends(get_service),
    db: Session = Depends(get_db),
) -> EventTypeResponse:
    """Get a specific event type by ID."""
    event_type = service.get_event_type(type_id, db)
    if not event_type:
        raise HTTPException(
            status_code=404, detail="Event type not found"
        )
    return event_type


@router.put("/{type_id}", response_model=EventTypeResponse)
def update_event_type(
    type_id: int,
    event_type_update: EventTypeUpdate,
    service: EventTypeService = Depends(get_service),
    db: Session = Depends(get_db),
) -> EventTypeResponse:
    """Update an event type."""
    event_type = service.update_event_type(
        type_id, event_type_update, db
    )
    if not event_type:
        raise HTTPException(
            status_code=404, detail="Event type not found"
        )
    return event_type


@router.delete("/{type_id}")
def delete_event_type(
    type_id: int,
    service: EventTypeService = Depends(get_service),
    db: Session = Depends(get_db),
) -> dict:
    """Delete an event type."""
    success = service.delete_event_type(type_id, db)
    if not success:
        raise HTTPException(
            status_code=404, detail="Event type not found"
        )
    return {
        "status": "success",
        "message": "Event type deleted",
    }
