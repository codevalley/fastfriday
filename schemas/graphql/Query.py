from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy.orm import Session

from schemas.graphql.types.models import (
    EventType,
    LifeEvent,
    LifeEventFilter,
)
from services.EventTypeService import EventTypeService
from services.LifeEventService import LifeEventService


def get_db(info: Info) -> Session:
    return info.context["db"]


@strawberry.type
class Query:
    @strawberry.field
    def event_type(
        self, info: Info, id: int
    ) -> Optional[EventType]:
        """Get an event type by ID"""
        db = get_db(info)
        service = EventTypeService(db)
        db_event_type = service.get_event_type(id)
        if not db_event_type:
            return None
        return EventType.from_db(db_event_type)

    @strawberry.field
    def event_types(
        self, info: Info, skip: int = 0, limit: int = 100
    ) -> List[EventType]:
        """Get all event types with pagination"""
        db = get_db(info)
        service = EventTypeService(db)
        db_event_types = service.get_event_types(
            skip, limit
        )
        return [
            EventType.from_db(et) for et in db_event_types
        ]

    @strawberry.field
    def life_event(
        self, info: Info, id: int
    ) -> Optional[LifeEvent]:
        """Get a life event by ID"""
        db = get_db(info)
        service = LifeEventService(db)
        db_event = service.get_event(id)
        if not db_event:
            return None
        return LifeEvent.from_db(db_event)

    @strawberry.field
    def life_events(
        self,
        info: Info,
        filter: Optional[LifeEventFilter] = None,
    ) -> List[LifeEvent]:
        """Get life events with optional filtering"""
        db = get_db(info)
        service = LifeEventService(db)
        filters = filter.__dict__ if filter else {}
        db_events = service.get_events(
            filters=filters,
            skip=filter.offset if filter else 0,
            limit=filter.limit if filter else 100,
        )
        return [LifeEvent.from_db(e) for e in db_events]
