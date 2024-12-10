from typing import List, Optional
from datetime import datetime

from fastapi import Depends, HTTPException
from models.LifeEventModel import LifeEvent
from models.EventTypeModel import EventType

from repositories.LifeEventRepository import (
    LifeEventRepository,
)
from repositories.EventTypeRepository import (
    EventTypeRepository,
)
from schemas.pydantic.LifeEventSchema import (
    LifeEventCreate,
    LifeEventUpdate,
)


class LifeEventService:
    life_event_repository: LifeEventRepository
    event_type_repository: EventTypeRepository

    def __init__(
        self,
        life_event_repository: LifeEventRepository = Depends(),
        event_type_repository: EventTypeRepository = Depends(),
    ) -> None:
        self.life_event_repository = life_event_repository
        self.event_type_repository = event_type_repository

    def create(
        self, event_data: LifeEventCreate
    ) -> LifeEvent:
        # Verify event type exists
        event_type = self.event_type_repository.get(
            event_data.event_type_id
        )
        if not event_type:
            raise HTTPException(
                status_code=404,
                detail="Event type not found",
            )

        life_event = LifeEvent(
            event_type_id=event_data.event_type_id,
            timestamp=event_data.timestamp,
            data=event_data.data,
        )
        return self.life_event_repository.create(life_event)

    def delete(self, event_id: int) -> None:
        return self.life_event_repository.delete(event_id)

    def get(self, event_id: int) -> LifeEvent:
        event = self.life_event_repository.get(event_id)
        if not event:
            raise HTTPException(
                status_code=404,
                detail="Life event not found",
            )
        return event

    def list(
        self,
        event_type_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: Optional[int] = 100,
        start: Optional[int] = 0,
    ) -> List[LifeEvent]:
        return self.life_event_repository.list(
            limit=limit,
            start=start,
            event_type_id=event_type_id,
            start_date=start_date,
            end_date=end_date,
        )

    def update(
        self, event_id: int, event_data: LifeEventUpdate
    ) -> LifeEvent:
        current_event = self.get(event_id)

        # Update only provided fields
        if event_data.timestamp is not None:
            setattr(
                current_event,
                "timestamp",
                event_data.timestamp,
            )
        if event_data.data is not None:
            setattr(current_event, "data", event_data.data)
        if (
            hasattr(event_data, "event_type_id")
            and event_data.event_type_id is not None
        ):
            event_type = self.event_type_repository.get(
                event_data.event_type_id
            )
            if not event_type:
                raise HTTPException(
                    status_code=404,
                    detail="Event type not found",
                )
            setattr(
                current_event,
                "event_type_id",
                event_data.event_type_id,
            )

        return self.life_event_repository.update(
            event_id, current_event
        )

    def get_event_type(
        self, event_id: int
    ) -> Optional[EventType]:
        event = self.get(event_id)
        return event.event_type if event else None
