"""Test cases for LifeEventModel."""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.LifeEventModel import LifeEvent
from models.EventTypeModel import EventType


@pytest.fixture
def sample_event_type(db: Session):
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
def sample_life_event(sample_event_type):
    """Create a sample life event for testing."""
    return {
        "timestamp": datetime.now(),
        "data": {"test_field": "test_value"},
        "event_type_id": sample_event_type.id,
    }


def test_create_life_event(db: Session, sample_life_event):
    """Test creating a life event."""
    event = LifeEvent(**sample_life_event)
    db.add(event)
    db.commit()
    db.refresh(event)

    assert event.id is not None
    assert isinstance(event.timestamp, datetime)
    assert event.data == sample_life_event["data"]
    assert (
        event.event_type_id
        == sample_life_event["event_type_id"]
    )


def test_event_type_relationship(
    db: Session, sample_life_event, sample_event_type
):
    """Test the relationship with event type."""
    event = LifeEvent(**sample_life_event)
    db.add(event)
    db.commit()
    db.refresh(event)

    assert event.event_type is not None
    assert event.event_type.id == sample_event_type.id
    assert event.event_type.name == sample_event_type.name


def test_event_type_required(db: Session):
    """Test that event_type_id is required."""
    event = LifeEvent(
        timestamp=datetime.now(),
        data={"test": "value"},
    )
    db.add(event)

    with pytest.raises(IntegrityError):
        db.commit()


def test_data_required(db: Session, sample_event_type):
    """Test that data field is required."""
    event = LifeEvent(
        timestamp=datetime.now(),
        event_type_id=sample_event_type.id,
    )
    db.add(event)

    with pytest.raises(IntegrityError):
        db.commit()


def test_timestamp_default(db: Session, sample_event_type):
    """Test that timestamp gets default value."""
    event = LifeEvent(
        data={"test": "value"},
        event_type_id=sample_event_type.id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    assert event.timestamp is not None
    assert isinstance(event.timestamp, datetime)


def test_string_representation(
    db: Session, sample_life_event
):
    """Test the string representation of life event."""
    event = LifeEvent(**sample_life_event)
    assert str(event) == (
        f"<LifeEvent {event.event_type_id}:"
        f"{event.timestamp}>"
    )


def test_event_name_property(
    db: Session, sample_life_event, sample_event_type
):
    """Test the event_name property."""
    event = LifeEvent(**sample_life_event)
    db.add(event)
    db.commit()
    db.refresh(event)

    assert event.event_name == sample_event_type.name


def test_cascade_delete_from_event_type(
    db: Session, sample_life_event
):
    """Test cascade delete when event type is deleted."""
    event = LifeEvent(**sample_life_event)
    db.add(event)
    db.commit()

    # Delete the event type
    event_type = (
        db.query(EventType)
        .filter_by(id=sample_life_event["event_type_id"])
        .first()
    )
    db.delete(event_type)
    db.commit()

    # Verify event was deleted
    deleted_event = (
        db.query(LifeEvent).filter_by(id=event.id).first()
    )
    assert deleted_event is None
