from typing import List, Optional

from fastapi import Depends, HTTPException
from models.EventTypeModel import EventType
from models.LifeEventModel import LifeEvent

from repositories.EventTypeRepository import (
    EventTypeRepository,
)
from schemas.pydantic.EventTypeSchema import (
    EventTypeCreate,
    EventTypeUpdate,
)


class EventTypeService:
    event_type_repository: EventTypeRepository

    def __init__(
        self,
        event_type_repository: EventTypeRepository = Depends(),
    ) -> None:
        self.event_type_repository = event_type_repository

    def create(
        self, event_type_data: EventTypeCreate
    ) -> EventType:
        event_type = EventType(
            name=event_type_data.name,
            description=event_type_data.description,
            event_schema=event_type_data.event_schema,
            icon=event_type_data.icon,
            color=event_type_data.color,
        )
        return self.event_type_repository.create(event_type)

    def delete(self, event_type_id: int) -> None:
        return self.event_type_repository.delete(
            event_type_id
        )

    def get(self, event_type_id: int) -> EventType:
        event_type = self.event_type_repository.get(
            event_type_id
        )
        if not event_type:
            raise HTTPException(
                status_code=404,
                detail="Event type not found",
            )
        return event_type

    def list(
        self,
        name: Optional[str] = None,
        limit: Optional[int] = 100,
        start: Optional[int] = 0,
    ) -> List[EventType]:
        return self.event_type_repository.list(
            limit=limit,
            start=start,
            name=name,
        )

    def update(
        self,
        event_type_id: int,
        event_type_data: EventTypeUpdate,
    ) -> EventType:
        current_event_type = self.get(event_type_id)

        # Update only provided fields
        if event_type_data.name is not None:
            setattr(
                current_event_type,
                "name",
                event_type_data.name,
            )
        if event_type_data.description is not None:
            setattr(
                current_event_type,
                "description",
                event_type_data.description,
            )
        if event_type_data.event_schema is not None:
            setattr(
                current_event_type,
                "event_schema",
                event_type_data.event_schema,
            )
        if event_type_data.icon is not None:
            setattr(
                current_event_type,
                "icon",
                event_type_data.icon,
            )
        if event_type_data.color is not None:
            setattr(
                current_event_type,
                "color",
                event_type_data.color,
            )

        return self.event_type_repository.update(
            event_type_id, current_event_type
        )

    def get_events(
        self, event_type_id: int
    ) -> List[LifeEvent]:
        event_type = self.get(event_type_id)
        return event_type.events if event_type else []
