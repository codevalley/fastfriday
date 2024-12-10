"""Test cases for EventTypeService."""

import pytest
from typing import Dict, Any
from sqlalchemy.orm import Session

from models.EventTypeModel import EventType
from services.EventTypeService import EventTypeService
from schemas.pydantic.EventTypeSchema import (
    EventTypeCreate,
    EventTypeUpdate,
)


@pytest.fixture
def service() -> EventTypeService:
    """Create a service instance for testing."""
    return EventTypeService()


@pytest.fixture
def sample_event_type() -> Dict[str, Any]:
    """Create a sample event type for testing."""
    return {
        "name": "test_event",
        "description": "Test event type",
        "event_schema": {
            "type": "object",
            "properties": {
                "test_field": {"type": "string"},
            },
        },
        "icon": "test_icon",
        "color": "#FF0000",
    }


def test_create_event_type(
    service: EventTypeService,
    db: Session,
    sample_event_type: Dict[str, Any],
) -> None:
    """Test creating a new event type."""
    event_type = EventTypeCreate(**sample_event_type)
    result = service.create_event_type(event_type, db)

    assert result.name == sample_event_type["name"]
    assert (
        result.description
        == sample_event_type["description"]
    )
    assert (
        result.event_schema
        == sample_event_type["event_schema"]
    )
    assert result.icon == sample_event_type["icon"]
    assert result.color == sample_event_type["color"]


def test_get_event_type(
    service: EventTypeService,
    db: Session,
    sample_event_type: Dict[str, Any],
) -> None:
    """Test retrieving an event type."""
    # Create test event type
    event_type = EventType(**sample_event_type)
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    # Get the actual ID value
    type_id = int(event_type.id)
    assert type_id is not None

    # Test retrieval
    result = service.get_event_type(type_id, db)
    assert result is not None
    assert result.name == sample_event_type["name"]


def test_get_event_types(
    service: EventTypeService,
    db: Session,
    sample_event_type: Dict[str, Any],
) -> None:
    """Test listing event types with pagination."""
    # Create multiple test event types
    for i in range(3):
        event_type = EventType(
            **{
                **sample_event_type,
                "name": f"test_event_{i}",
            }
        )
        db.add(event_type)
    db.commit()

    # Test pagination
    results = service.get_event_types(
        skip=0, limit=2, db=db
    )
    assert len(results) == 2
    assert all(isinstance(r.id, int) for r in results)


def test_update_event_type(
    service: EventTypeService,
    db: Session,
    sample_event_type: Dict[str, Any],
) -> None:
    """Test updating an event type."""
    # Create test event type
    event_type = EventType(**sample_event_type)
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    # Get the actual ID value
    type_id = int(event_type.id)
    assert type_id is not None

    # Update event type
    update_data = EventTypeUpdate(
        name="updated_test_event",
        description="Updated description",
    )
    result = service.update_event_type(
        type_id, update_data, db
    )

    assert result is not None
    assert result.name == "updated_test_event"
    assert result.description == "Updated description"


def test_delete_event_type(
    service: EventTypeService,
    db: Session,
    sample_event_type: Dict[str, Any],
) -> None:
    """Test deleting an event type."""
    # Create test event type
    event_type = EventType(**sample_event_type)
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    # Get the actual ID value
    type_id = int(event_type.id)
    assert type_id is not None

    # Test deletion
    result = service.delete_event_type(type_id, db)
    assert result is True

    # Verify deletion
    deleted = service.get_event_type(type_id, db)
    assert deleted is None


def test_get_nonexistent_event_type(
    service: EventTypeService, db: Session
) -> None:
    """Test retrieving a non-existent event type."""
    result = service.get_event_type(999, db)
    assert result is None


def test_update_nonexistent_event_type(
    service: EventTypeService, db: Session
) -> None:
    """Test updating a non-existent event type."""
    update_data = EventTypeUpdate(name="test")
    result = service.update_event_type(999, update_data, db)
    assert result is None


def test_delete_nonexistent_event_type(
    service: EventTypeService, db: Session
) -> None:
    """Test deleting a non-existent event type."""
    result = service.delete_event_type(999, db)
    assert result is False
