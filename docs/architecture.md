# Clean Architecture Implementation for Friday - Personal Life Logger

## Overview

This project implements the Clean Architecture (also known as Hexagonal Architecture) pattern for Friday, a personal life logging system. The architecture emphasizes separation of concerns and dependency inversion, organized in concentric circles, with the domain layer at the center and external concerns at the outer layers.

## Architectural Principles

1. **Independence of Frameworks**: The life logging business logic is isolated from the delivery mechanism (FastAPI) and external frameworks.
2. **Testability**: The architecture makes the system highly testable by isolating life logging components.
3. **Independence of UI**: The system works with multiple interfaces (REST, GraphQL) for accessing life events.
4. **Independence of Database**: The life logging rules don't know about how events are stored.
5. **Independence of External Agency**: Life logging business rules are separate from external integrations.

## Layer Details

### 1. Domain Layer (Inner Circle)

Located in `models/`, this layer contains:
- Core business entities (LifeEvent, EventType)
- Business rules for life event validation and processing
- Interface definitions for life logging operations
- No dependencies on outer layers

Example:
```python
# models/LifeEventModel.py - Core domain entity
class LifeEventModel(Base):
    __tablename__ = "life_events"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    event_type_id = Column(Integer, ForeignKey("event_types.id"))
    data = Column(JSON)  # Flexible schema for different event types
    tags = Column(ARRAY(String))  # Event categorization
    location = Column(JSON, nullable=True)  # Optional location data
    
    # Relationships
    event_type = relationship("EventTypeModel", back_populates="events")
```

### 2. Application Layer

Located in `services/`, this layer:
- Implements life logging use cases (create event, query events, analyze patterns)
- Orchestrates the flow of life event data
- Contains business logic for event processing and validation
- Depends only on the domain layer

Example:
```python
# services/LifeEventService.py - Application service
class LifeEventService:
    def __init__(self, repository: LifeEventRepository):
        self._repository = repository
    
    async def create_event(self, event_data: dict) -> LifeEventModel:
        # Validate event type
        event_type = await self._validate_event_type(event_data["type"])
        
        # Validate event data against type schema
        self._validate_event_data(event_data["data"], event_type.schema)
        
        # Create and store the life event
        event = LifeEventModel(
            timestamp=event_data["timestamp"],
            event_type_id=event_type.id,
            data=event_data["data"],
            tags=event_data.get("tags", []),
            location=event_data.get("location")
        )
        return await self._repository.create(event)
    
    async def query_events(self, filters: dict) -> List[LifeEventModel]:
        # Query events with time range, type, tags, etc.
        return await self._repository.query(filters)
```

### 3. Interface Adapters

Located in `repositories/` and `routers/`, this layer:
- Converts life event data between domain and external formats
- Implements repository interfaces for event storage and retrieval
- Handles HTTP/GraphQL requests for life logging operations
- Contains controllers and presenters for life event data

### 4. External Interfaces

Located in various outer layer directories:
- REST API endpoints for life events (`routers/v1/events.py`)
- GraphQL schema for event queries (`schemas/graphql/`)
- Database configurations for event storage (`configs/`)
- External service integrations (photo storage, activity tracking, location services)

## Dependency Flow

The dependencies flow from the outer layers inward:
```
External Layer (REST/GraphQL) → Interface Adapters → Application Services → Domain Model
                                                                       ↑
                                                            Core Life Logging Logic
```

## Key Implementation Patterns

1. **Dependency Injection**
   - Used throughout the life logging system
   - Facilitates testing and loose coupling
   - Implemented using FastAPI's dependency injection system
   - Example: Injecting event repositories and services

2. **Repository Pattern**
   - Abstracts life event data persistence
   - Allows swapping of event storage systems
   - Implements CRUD operations for events and types
   - Supports efficient event querying and filtering

3. **DTO Pattern**
   - Separates life event domain models from API contracts
   - Handles event data validation and transformation
   - Implements using Pydantic models for type safety

## Benefits of This Architecture

1. **Maintainability**: Changes in external layers don't affect the core life logging logic
2. **Testability**: Each life logging component can be tested in isolation
3. **Flexibility**: Easy to add new event types or change storage systems
4. **Scalability**: Clear boundaries make it easier to scale event processing
5. **Data Privacy**: Strong separation of concerns for handling personal life data
6. **Extensibility**: Simple to add new event types or analysis capabilities