"""Test cases for LifeEventService."""

import pytest
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from models.LifeEventModel import LifeEvent
from models.EventTypeModel import EventType
from services.LifeEventService import LifeEventService
from schemas.pydantic.LifeEventSchema import (
    LifeEventCreate,
    LifeEventUpdate,
)


@pytest.fixture
def service() -> LifeEventService:
    """Create a service instance for testing."""
    return LifeEventService()


@pytest.fixture
def sample_event_type(db: Session) -> EventType:
    """Create a sample event type for testing."""
    event_type = EventType(
        name="test_type",
        description="Test event type",
        event_schema={
            "type": "object",
            "properties": {
                "test_field": {"type": "string"},
            },
        },
    )
    db.add(event_type)
    db.commit()
    db.refresh(event_type)
    return event_type


@pytest.fixture
def sample_life_event(sample_event_type) -> Dict[str, Any]:
    """Create a sample life event for testing."""
    return {
        "timestamp": datetime.now(),
        "data": {"test_field": "test_value"},
        "event_type_id": sample_event_type.id,
    }


def test_create_event(
    service: LifeEventService,
    db: Session,
    sample_life_event: Dict[str, Any],
) -> None:
    """Test creating a new life event."""
    event = LifeEventCreate(**sample_life_event)
    result = service.create_event(event, db)

    assert result.data == sample_life_event["data"]
    assert (
        result.event_type_id
        == sample_life_event["event_type_id"]
    )


def test_get_events(
    service: LifeEventService,
    db: Session,
    sample_life_event: Dict[str, Any],
) -> None:
    """Test listing life events with filtering."""
    # Create multiple test events
    for i in range(3):
        event = LifeEvent(
            **{
                **sample_life_event,
                "data": {"test_field": f"test_value_{i}"},
            }
        )
        db.add(event)
    db.commit()

    # Test filtering and pagination
    filters: Dict[str, Any] = {}
    results = service.get_events(
        filters, skip=0, limit=2, db=db
    )
    assert len(results) == 2
    assert all(isinstance(r.id, int) for r in results)


def test_get_events_with_date_filter(
    service: LifeEventService,
    db: Session,
    sample_life_event: Dict[str, Any],
) -> None:
    """Test event filtering by date."""
    # Create test events with different dates
    event1 = LifeEvent(**sample_life_event)
    event2 = LifeEvent(
        **{
            **sample_life_event,
            "timestamp": datetime(2024, 1, 1),
        }
    )
    db.add_all([event1, event2])
    db.commit()

    # Test date filtering
    date_filters: Dict[str, Any] = {
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
    }
    results = service.get_events(
        date_filters, skip=0, limit=10, db=db
    )
    assert len(results) == 1


def test_update_event(
    service: LifeEventService,
    db: Session,
    sample_life_event: Dict[str, Any],
) -> None:
    """Test updating a life event."""
    # Create test event
    event = LifeEvent(**sample_life_event)
    db.add(event)
    db.commit()
    db.refresh(event)

    # Update event
    update_data = LifeEventUpdate(
        data={"test_field": "updated_value"}
    )
    result = service.update_event(event.id, update_data, db)

    assert result is not None
    assert result.data["test_field"] == "updated_value"


def test_delete_event(
    service: LifeEventService,
    db: Session,
    sample_life_event: Dict[str, Any],
) -> None:
    """Test deleting a life event."""
    # Create test event
    event = LifeEvent(**sample_life_event)
    db.add(event)
    db.commit()
    db.refresh(event)

    # Delete event
    result = service.delete_event(event.id, db)
    assert result is True

    # Verify deletion
    deleted = service.get_event(event.id, db)
    assert deleted is None
