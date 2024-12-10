from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from models.LifeEventModel import LifeEvent
from models.EventTypeModel import EventType
from schemas.pydantic.LifeEventSchema import (
    LifeEventCreate,
    LifeEventUpdate,
    LifeEventResponse,
)


class LifeEventService:
    def __init__(self):
        """Initialize service without database dependency."""
        pass

    def create_event(
        self, event: LifeEventCreate, db: Session
    ) -> LifeEventResponse:
        """Create a new life event."""
        # Verify event type exists
        event_type = (
            db.query(EventType)
            .filter(EventType.id == event.event_type_id)
            .first()
        )
        if not event_type:
            raise ValueError("Event type not found")

        db_event = LifeEvent(
            timestamp=event.timestamp,
            data=event.data,
            tags=event.tags,
            location=event.location,
            event_type_id=event.event_type_id,
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return LifeEventResponse.from_orm(db_event)

    def get_event(
        self, event_id: int, db: Session
    ) -> Optional[LifeEventResponse]:
        """Get a life event by ID."""
        db_event = (
            db.query(LifeEvent)
            .filter(LifeEvent.id == event_id)
            .first()
        )
        if not db_event:
            return None
        return LifeEventResponse.from_orm(db_event)

    def get_events(
        self,
        filters: Dict[str, Any],
        skip: int,
        limit: int,
        db: Session,
    ) -> List[LifeEventResponse]:
        """Get life events with filtering and pagination."""
        query = db.query(LifeEvent)

        if filters.get("event_type"):
            query = query.join(EventType).filter(
                EventType.name == filters["event_type"]
            )

        if filters.get("start_date"):
            start_date = datetime.fromisoformat(
                filters["start_date"]
            )
            query = query.filter(
                LifeEvent.timestamp >= start_date
            )

        if filters.get("end_date"):
            end_date = datetime.fromisoformat(
                filters["end_date"]
            )
            query = query.filter(
                LifeEvent.timestamp <= end_date
            )

        if filters.get("tags"):
            for tag in filters["tags"]:
                query = query.filter(
                    LifeEvent.tags.contains([tag])
                )

        db_events = query.offset(skip).limit(limit).all()
        return [
            LifeEventResponse.from_orm(event)
            for event in db_events
        ]

    def update_event(
        self,
        event_id: int,
        event: LifeEventUpdate,
        db: Session,
    ) -> Optional[LifeEventResponse]:
        """Update a life event."""
        db_event = (
            db.query(LifeEvent)
            .filter(LifeEvent.id == event_id)
            .first()
        )
        if not db_event:
            return None

        update_data = event.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)

        db.commit()
        db.refresh(db_event)
        return LifeEventResponse.from_orm(db_event)

    def delete_event(
        self, event_id: int, db: Session
    ) -> bool:
        """Delete a life event."""
        db_event = (
            db.query(LifeEvent)
            .filter(LifeEvent.id == event_id)
            .first()
        )
        if not db_event:
            return False

        db.delete(db_event)
        db.commit()
        return True
