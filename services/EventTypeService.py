from typing import List, Optional
from sqlalchemy.orm import Session

from models.EventTypeModel import EventType
from schemas.pydantic.EventTypeSchema import (
    EventTypeCreate,
    EventTypeUpdate,
    EventTypeResponse,
)


class EventTypeService:
    def __init__(self):
        """Initialize service without database dependency."""
        pass

    def create_event_type(
        self, event_type: EventTypeCreate, db: Session
    ) -> EventTypeResponse:
        """Create a new event type."""
        db_event_type = EventType(
            name=event_type.name,
            description=event_type.description,
            event_schema=event_type.event_schema,
            icon=event_type.icon,
            color=event_type.color,
        )
        db.add(db_event_type)
        db.commit()
        db.refresh(db_event_type)
        return EventTypeResponse.from_orm(db_event_type)

    def get_event_type(
        self, type_id: int, db: Session
    ) -> Optional[EventTypeResponse]:
        """Get an event type by ID."""
        db_event_type = (
            db.query(EventType)
            .filter(EventType.id == type_id)
            .first()
        )
        if not db_event_type:
            return None
        return EventTypeResponse.from_orm(db_event_type)

    def get_event_types(
        self, skip: int, limit: int, db: Session
    ) -> List[EventTypeResponse]:
        """Get all event types with pagination."""
        db_event_types = (
            db.query(EventType)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            EventTypeResponse.from_orm(et)
            for et in db_event_types
        ]

    def update_event_type(
        self,
        type_id: int,
        event_type: EventTypeUpdate,
        db: Session,
    ) -> Optional[EventTypeResponse]:
        """Update an event type."""
        db_event_type = (
            db.query(EventType)
            .filter(EventType.id == type_id)
            .first()
        )
        if not db_event_type:
            return None

        update_data = event_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event_type, field, value)

        db.commit()
        db.refresh(db_event_type)
        return EventTypeResponse.from_orm(db_event_type)

    def delete_event_type(
        self, type_id: int, db: Session
    ) -> bool:
        """Delete an event type."""
        db_event_type = (
            db.query(EventType)
            .filter(EventType.id == type_id)
            .first()
        )
        if not db_event_type:
            return False

        db.delete(db_event_type)
        db.commit()
        return True
