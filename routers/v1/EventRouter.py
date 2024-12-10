from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends
from services.LifeEventService import LifeEventService
from schemas.pydantic.LifeEventSchema import (
    LifeEventResponse,
    LifeEventCreate,
    LifeEventUpdate,
)

router = APIRouter(
    prefix="/api/v1/events",
    tags=["Life Events"],
)


@router.post("/", response_model=LifeEventResponse)
def create_event(
    event: LifeEventCreate,
    service: LifeEventService = Depends(),
) -> LifeEventResponse:
    """Create a new life event."""
    db_event = service.create(event)
    return LifeEventResponse.from_orm(db_event)


@router.get("/", response_model=List[LifeEventResponse])
def list_events(
    event_type_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: Optional[int] = 100,
    start: Optional[int] = 0,
    service: LifeEventService = Depends(),
) -> List[LifeEventResponse]:
    """List all life events."""
    db_events = service.list(
        event_type_id=event_type_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        start=start,
    )
    return [
        LifeEventResponse.from_orm(event)
        for event in db_events
    ]


@router.get("/{event_id}", response_model=LifeEventResponse)
def get_event(
    event_id: int,
    service: LifeEventService = Depends(),
) -> LifeEventResponse:
    """Get a specific life event."""
    db_event = service.get(event_id)
    return LifeEventResponse.from_orm(db_event)


@router.put("/{event_id}", response_model=LifeEventResponse)
def update_event(
    event_id: int,
    event: LifeEventUpdate,
    service: LifeEventService = Depends(),
) -> LifeEventResponse:
    """Update a life event."""
    db_event = service.update(event_id, event)
    return LifeEventResponse.from_orm(db_event)


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    service: LifeEventService = Depends(),
) -> None:
    """Delete a life event."""
    return service.delete(event_id)
