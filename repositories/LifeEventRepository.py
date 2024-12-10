from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import and_

from configs.database import get_db
from models.LifeEventModel import LifeEvent
from repositories.RepositoryMeta import RepositoryMeta


class LifeEventRepository(RepositoryMeta[LifeEvent, int]):
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
    ) -> List[LifeEvent]:
        query = self.db.query(LifeEvent)

        filter_conditions = []

        # Handle direct kwargs
        event_type_id = kwargs.get("event_type_id")
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")

        if event_type_id:
            filter_conditions.append(
                LifeEvent.event_type_id == event_type_id
            )
        if start_date:
            filter_conditions.append(
                LifeEvent.timestamp >= start_date
            )
        if end_date:
            filter_conditions.append(
                LifeEvent.timestamp <= end_date
            )

        # Apply additional filters from the filters dict
        if filters:
            if "event_type_id" in filters:
                filter_conditions.append(
                    LifeEvent.event_type_id
                    == filters["event_type_id"]
                )
            if "start_date" in filters:
                filter_conditions.append(
                    LifeEvent.timestamp
                    >= filters["start_date"]
                )
            if "end_date" in filters:
                filter_conditions.append(
                    LifeEvent.timestamp
                    <= filters["end_date"]
                )

        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        if start is not None:
            query = query.offset(start)
        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get(self, id: int) -> Optional[LifeEvent]:
        return self.db.get(
            LifeEvent,
            id,
            options=[lazyload(LifeEvent.event_type)],
        )

    def create(self, life_event: LifeEvent) -> LifeEvent:
        self.db.add(life_event)
        self.db.commit()
        self.db.refresh(life_event)
        return life_event

    def update(
        self, id: int, life_event: LifeEvent
    ) -> LifeEvent:
        # Handle the id assignment without type issues
        setattr(life_event, "id", id)
        self.db.merge(life_event)
        self.db.commit()
        return life_event

    def delete(self, id: int) -> None:
        life_event = self.get(id)
        if life_event:
            self.db.delete(life_event)
            self.db.commit()
            self.db.flush()
