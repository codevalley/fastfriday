from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.LifeEventModel import LifeEvent  # noqa: F401
from models.EventTypeModel import EventType  # noqa: F401
from schemas.pydantic.LifeEventSchema import (
    LifeEventCreate,
    LifeEventResponse,
    LifeEventUpdate,
)
from services.LifeEventService import LifeEventService
from configs.database import get_db

router = APIRouter(
    prefix="/api/v1/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


def get_service() -> LifeEventService:
    """Get service instance."""
    return LifeEventService()


@router.post("/", response_model=LifeEventResponse)
def create_event(
    event: LifeEventCreate,
    service: LifeEventService = Depends(get_service),
    db: Session = Depends(get_db),
) -> LifeEventResponse:
    """Create a new life event."""
    return service.create_event(event, db)


@router.get("/", response_model=List[LifeEventResponse])
def list_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    service: LifeEventService = Depends(get_service),
    db: Session = Depends(get_db),
) -> List[LifeEventResponse]:
    """List life events with optional filtering."""
    filters = {
        "event_type": event_type,
        "start_date": start_date,
        "end_date": end_date,
        "tags": tags,
    }
    return service.get_events(filters, skip, limit, db)


@router.get("/{event_id}", response_model=LifeEventResponse)
def get_event(
    event_id: int,
    service: LifeEventService = Depends(get_service),
    db: Session = Depends(get_db),
) -> LifeEventResponse:
    """Get a specific life event by ID."""
    event = service.get_event(event_id, db)
    if not event:
        raise HTTPException(
            status_code=404, detail="Event not found"
        )
    return event


@router.put("/{event_id}", response_model=LifeEventResponse)
def update_event(
    event_id: int,
    event_update: LifeEventUpdate,
    service: LifeEventService = Depends(get_service),
    db: Session = Depends(get_db),
) -> LifeEventResponse:
    """Update a life event."""
    event = service.update_event(event_id, event_update, db)
    if not event:
        raise HTTPException(
            status_code=404, detail="Event not found"
        )
    return event


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    service: LifeEventService = Depends(get_service),
    db: Session = Depends(get_db),
) -> dict:
    """Delete a life event."""
    success = service.delete_event(event_id, db)
    if not success:
        raise HTTPException(
            status_code=404, detail="Event not found"
        )
    return {"status": "success", "message": "Event deleted"}
