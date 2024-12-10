from typing import List, Optional, Dict, Any

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from configs.database import get_db
from models.EventTypeModel import EventType
from repositories.RepositoryMeta import RepositoryMeta


class EventTypeRepository(RepositoryMeta[EventType, int]):
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    def list(
        self,
        limit: Optional[int] = None,
        start: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[EventType]:
        query = self.db.query(EventType)

        name = kwargs.get("name")
        if name:
            query = query.filter(EventType.name == name)
        elif filters and "name" in filters:
            query = query.filter(
                EventType.name == filters["name"]
            )

        if start is not None:
            query = query.offset(start)
        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get(self, id: int) -> Optional[EventType]:
        return self.db.get(
            EventType,
            id,
            options=[lazyload(EventType.events)],
        )

    def create(self, event_type: EventType) -> EventType:
        self.db.add(event_type)
        self.db.commit()
        self.db.refresh(event_type)
        return event_type

    def update(
        self, id: int, event_type: EventType
    ) -> EventType:
        # Handle the id assignment without type issues
        setattr(event_type, "id", id)
        self.db.merge(event_type)
        self.db.commit()
        return event_type

    def delete(self, id: int) -> None:
        event_type = self.get(id)
        if event_type:
            self.db.delete(event_type)
            self.db.commit()
            self.db.flush()
