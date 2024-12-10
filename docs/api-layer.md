# API Layer Documentation

## Overview

Friday's API layer provides both REST and GraphQL interfaces for interacting with life events. The API is designed to be intuitive, efficient, and flexible, allowing clients to record and retrieve life events in various formats.

## REST API Implementation

### Event Types API

```python
@router.get("/api/v1/event-types")
async def list_event_types() -> List[EventType]:
    """Get all available event types"""

@router.get("/api/v1/event-types/{type_id}")
async def get_event_type(type_id: int) -> EventType:
    """Get a specific event type and its schema"""

@router.post("/api/v1/event-types")
async def create_event_type(event_type: EventTypeCreate) -> EventType:
    """Create a new event type"""
```

### Life Events API

```python
@router.post("/api/v1/events")
async def create_event(event: LifeEventCreate) -> LifeEvent:
    """Record a new life event"""

@router.get("/api/v1/events")
async def list_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    event_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[LifeEvent]:
    """Get life events with optional filtering"""

@router.get("/api/v1/events/{event_id}")
async def get_event(event_id: int) -> LifeEvent:
    """Get a specific life event"""

@router.delete("/api/v1/events/{event_id}")
async def delete_event(event_id: int) -> None:
    """Delete a life event"""
```

## GraphQL API Implementation

### Schema Definition

```graphql
type EventType {
  id: ID!
  name: String!
  description: String
  schema: JSON
  icon: String
  color: String
  events: [LifeEvent!]!
}

type LifeEvent {
  id: ID!
  timestamp: DateTime!
  eventType: EventType!
  data: JSON!
}

type Query {
  eventTypes: [EventType!]!
  eventType(id: ID!): EventType
  events(
    startDate: DateTime
    endDate: DateTime
    eventType: String
    limit: Int = 50
    offset: Int = 0
  ): [LifeEvent!]!
  event(id: ID!): LifeEvent
}

type Mutation {
  createEvent(
    eventTypeId: ID!
    timestamp: DateTime
    data: JSON!
  ): LifeEvent!
  
  deleteEvent(id: ID!): Boolean!
  
  createEventType(
    name: String!
    description: String
    schema: JSON!
    icon: String
    color: String
  ): EventType!
}
```

## Request/Response Examples

### REST Examples

1. Creating a Photo Event:
```http
POST /api/v1/events
{
  "event_type_id": 1,
  "data": {
    "photo_url": "https://example.com/photo.jpg",
    "location": {
      "lat": 37.7749,
      "lng": -122.4194
    },
    "caption": "Beautiful sunset"
  }
}
```

2. Querying Events:
```http
GET /api/v1/events?event_type=exercise&start_date=2024-01-01T00:00:00Z
```

### GraphQL Examples

1. Querying Events with Type Information:
```graphql
query {
  events(eventType: "exercise", limit: 10) {
    id
    timestamp
    eventType {
      name
      icon
    }
    data
  }
}
```

2. Creating a Meal Event:
```graphql
mutation {
  createEvent(
    eventTypeId: 2
    data: {
      meal_type: "lunch",
      foods: [
        {
          name: "Salad",
          quantity: "1 bowl",
          calories: 200
        }
      ]
    }
  ) {
    id
    timestamp
    data
  }
}
```

## API Features

1. **Data Validation**
   - JSON Schema validation per event type
   - Type checking and required fields
   - Custom validation rules

2. **Query Flexibility**
   - Temporal filtering
   - Event type filtering
   - Pagination support
   - Rich GraphQL queries

3. **Performance**
   - Efficient database queries
   - Proper indexing
   - Response caching where appropriate

4. **Error Handling**
   - Consistent error responses
   - Detailed validation errors
   - Proper HTTP status codes

## Security Considerations

1. **Authentication**
   - JWT-based authentication
   - Secure token handling
   - Session management

2. **Authorization**
   - Event ownership validation
   - Role-based access control
   - Resource-level permissions

3. **Data Protection**
   - Input sanitization
   - Output encoding
   - Rate limiting

## Documentation

The API is documented using:
1. OpenAPI (Swagger) for REST endpoints
2. GraphQL Playground for GraphQL interface
3. Automatic schema generation
4. Interactive documentation at `/docs` and `/graphql`