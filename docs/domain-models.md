# Domain Models

## Overview

Friday's domain model is built around the concept of life events - discrete moments or activities in a person's life that they want to record and analyze. The model is designed to be flexible and extensible, allowing for various types of life events to be recorded with their specific data structures.

## Core Entities

### EventType

EventType defines a category of life events and provides metadata about how these events should be structured and displayed.

```python
class EventType:
    id: Integer           # Primary key
    name: String         # Unique identifier (e.g., "photo", "meal")
    description: String  # Human-readable description
    schema: JSON        # JSON Schema for validating event data
    icon: String        # UI icon identifier
    color: String       # Hex color code for UI
    events: List[LifeEvent]  # Related life events
```

#### JSON Schema Validation
Each EventType includes a JSON schema that defines the structure and validation rules for its associated events. For example:

```json
{
    "name": "meal",
    "schema": {
        "type": "object",
        "required": ["meal_type", "foods"],
        "properties": {
            "meal_type": {
                "type": "string",
                "enum": ["breakfast", "lunch", "dinner", "snack"]
            },
            "foods": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "quantity": {"type": "string"},
                        "calories": {"type": "number"}
                    }
                }
            }
        }
    }
}
```

### LifeEvent

LifeEvent represents a single moment or activity in a person's life. It combines fixed metadata with flexible JSON data.

```python
class LifeEvent:
    id: Integer          # Primary key
    timestamp: DateTime  # When the event occurred (indexed)
    event_type_id: Integer  # Reference to EventType
    data: JSON          # Event-specific data following type's schema
    event_type: EventType   # Related event type
```

#### Example Event Data
```json
// Photo Event
{
    "photo_url": "https://example.com/photo.jpg",
    "location": {
        "lat": 37.7749,
        "lng": -122.4194
    },
    "caption": "Beautiful sunset at Golden Gate Bridge"
}

// Exercise Event
{
    "type": "running",
    "duration": 1800,
    "distance": 5.2,
    "heart_rate": {
        "avg": 145,
        "max": 165
    }
}
```

## Design Decisions

1. **Flexible Data Storage**
   - Using JSON for event data allows for:
     - Different data structures per event type
     - Easy addition of new event types
     - Schema evolution without database migrations
     - Rich data storage with nested structures

2. **Schema Validation**
   - JSON Schema in EventType ensures:
     - Data consistency
     - Type safety
     - Required field validation
     - Enumerated values where appropriate

3. **Performance Considerations**
   - Indexed fields:
     - `timestamp` for temporal queries
     - `event_type_id` for filtering
     - `id` for lookups
   - Timezone support in timestamps

4. **Relationships**
   - One-to-many between EventType and LifeEvent
   - Cascade deletion of events when type is deleted
   - Bidirectional relationships for efficient querying

## Built-in Event Types

Friday comes with several pre-defined event types:

1. **Photo Events**
   - Capture moments with images
   - Support for location and captions
   - Optional tagging

2. **Meal Events**
   - Track food consumption
   - Categorize by meal type
   - Record individual food items and calories

3. **Exercise Events**
   - Log physical activities
   - Track duration and intensity
   - Support for various exercise types

4. **Note Events**
   - Quick text notes or thoughts
   - Support for tags and mood
   - Minimal structure for flexibility

5. **Sleep Events**
   - Track sleep patterns
   - Record quality and interruptions
   - Support for sleep cycle analysis

## Usage Examples

```python
# Creating a new meal event
meal_event = LifeEvent(
    event_type_id=2,  # meal type
    data={
        "meal_type": "lunch",
        "foods": [
            {"name": "Salad", "quantity": "1 bowl", "calories": 200},
            {"name": "Grilled Chicken", "quantity": "200g", "calories": 330}
        ],
        "location": "Home",
        "mood": "satisfied"
    }
)

# Creating a new exercise event
exercise_event = LifeEvent(
    event_type_id=3,  # exercise type
    data={
        "type": "running",
        "duration": 1800,  # in seconds
        "distance": 5.2,   # in kilometers
        "heart_rate": {
            "avg": 145,
            "max": 165
        }
    }
)
```