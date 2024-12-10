from typing import Optional
import strawberry
from strawberry.types import Info

from schemas.graphql.types.models import (
    EventType,
    EventTypeInput,
    EventTypeUpdate,
    LifeEvent,
    LifeEventInput,
    LifeEventUpdate,
)
from services.EventTypeService import EventTypeService
from services.LifeEventService import LifeEventService


def get_event_type_service(request) -> EventTypeService:
    return request.state.event_type_service


def get_life_event_service(request) -> LifeEventService:
    return request.state.life_event_service


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_event_type(
        self, info: Info, input: EventTypeInput
    ) -> EventType:
        """Create a new event type"""
        service = get_event_type_service(
            info.context["request"]
        )
        return await service.create_event_type(
            input.__dict__
        )

    @strawberry.mutation
    async def update_event_type(
        self, info: Info, id: int, input: EventTypeUpdate
    ) -> Optional[EventType]:
        """Update an existing event type"""
        service = get_event_type_service(
            info.context["request"]
        )
        return await service.update_event_type(
            id, input.__dict__
        )

    @strawberry.mutation
    async def delete_event_type(
        self, info: Info, id: int
    ) -> bool:
        """Delete an event type"""
        service = get_event_type_service(
            info.context["request"]
        )
        return await service.delete_event_type(id)

    @strawberry.mutation
    async def create_life_event(
        self, info: Info, input: LifeEventInput
    ) -> LifeEvent:
        """Create a new life event"""
        service = get_life_event_service(
            info.context["request"]
        )
        return await service.create_event(input.__dict__)

    @strawberry.mutation
    async def update_life_event(
        self, info: Info, id: int, input: LifeEventUpdate
    ) -> Optional[LifeEvent]:
        """Update an existing life event"""
        service = get_life_event_service(
            info.context["request"]
        )
        return await service.update_event(
            id, input.__dict__
        )

    @strawberry.mutation
    async def delete_life_event(
        self, info: Info, id: int
    ) -> bool:
        """Delete a life event"""
        service = get_life_event_service(
            info.context["request"]
        )
        return await service.delete_event(id)
