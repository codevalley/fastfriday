"""Test cases for EventTypeModel."""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.EventTypeModel import EventType
from models.LifeEventModel import LifeEvent


@pytest.fixture
def sample_event_type():
    """Create a sample event type for testing."""
    return {
        "name": "test_type",
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


def test_create_event_type(db: Session, sample_event_type):
    """Test creating an event type."""
    event_type = EventType(**sample_event_type)
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    assert event_type.id is not None
    assert event_type.name == sample_event_type["name"]
    assert (
        event_type.description
        == sample_event_type["description"]
    )
    assert (
        event_type.event_schema
        == sample_event_type["event_schema"]
    )
    assert event_type.icon == sample_event_type["icon"]
    assert event_type.color == sample_event_type["color"]


def test_unique_name_constraint(
    db: Session, sample_event_type
):
    """Test that event type names must be unique."""
    # Create first event type
    event_type1 = EventType(**sample_event_type)
    db.add(event_type1)
    db.commit()

    # Try to create second event type with same name
    event_type2 = EventType(**sample_event_type)
    db.add(event_type2)

    with pytest.raises(IntegrityError):
        db.commit()


def test_cascade_delete(db: Session, sample_event_type):
    """Test that deleting event type cascades to events."""
    # Create event type
    event_type = EventType(**sample_event_type)
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    # Create associated event
    event = LifeEvent(
        event_type_id=event_type.id,
        data={"test_field": "test_value"},
    )
    db.add(event)
    db.commit()

    # Delete event type
    db.delete(event_type)
    db.commit()

    # Verify event was also deleted
    events = db.query(LifeEvent).all()
    assert len(events) == 0


def test_nullable_fields(db: Session):
    """Test that optional fields can be null."""
    event_type = EventType(name="test_type")
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    assert event_type.description is None
    assert event_type.event_schema is None
    assert event_type.icon is None
    assert event_type.color is None


def test_string_representation(
    db: Session, sample_event_type
):
    """Test the string representation of event type."""
    event_type = EventType(**sample_event_type)
    assert (
        str(event_type) == f"<EventType {event_type.name}>"
    )


def test_relationships(db: Session, sample_event_type):
    """Test event type relationships."""
    # Create event type
    event_type = EventType(**sample_event_type)
    db.add(event_type)
    db.commit()
    db.refresh(event_type)

    # Create multiple associated events
    events = [
        LifeEvent(
            event_type_id=event_type.id,
            data={"test_field": f"value_{i}"},
        )
        for i in range(3)
    ]
    db.add_all(events)
    db.commit()

    # Test relationship
    assert len(event_type.events) == 3
    assert all(
        isinstance(event, LifeEvent)
        for event in event_type.events
    )
