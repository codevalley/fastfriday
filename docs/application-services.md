# Application Services Layer

## Overview

The application services layer implements the business logic and use cases for Friday's life logging functionality. Located in the `services/` directory, this layer orchestrates the flow of data and enforces business rules for life event recording and retrieval.

## Service Components

### 1. Event Type Service

```python
# services/EventTypeService.py
class EventTypeService:
    def __init__(self, repository: EventTypeRepository):
        self._repository = repository

    async def create_event_type(self, type_data: dict) -> EventType:
        """Create a new event type with schema validation"""
        # Validate JSON schema format
        self._validate_schema(type_data.get('schema'))
        return await self._repository.create(type_data)

    async def get_event_type(self, type_id: int) -> EventType:
        """Get event type by ID"""
        return await self._repository.get_by_id(type_id)

    async def get_event_type_by_name(self, name: str) -> EventType:
        """Get event type by unique name"""
        return await self._repository.get_by_name(name)

    def _validate_schema(self, schema: dict) -> None:
        """Validate that the provided JSON schema is valid"""
        try:
            jsonschema.validate({}, schema)  # Validate empty object to check schema
        except jsonschema.exceptions.SchemaError as e:
            raise ValidationError(f"Invalid JSON schema: {str(e)}")
```

### 2. Life Event Service

```python
# services/LifeEventService.py
class LifeEventService:
    def __init__(
        self,
        event_repository: LifeEventRepository,
        type_service: EventTypeService
    ):
        self._repository = event_repository
        self._type_service = type_service

    async def create_event(self, event_data: dict) -> LifeEvent:
        """Create a new life event with data validation"""
        # Get event type and validate data against schema
        event_type = await self._type_service.get_event_type(
            event_data['event_type_id']
        )
        self._validate_event_data(event_type.schema, event_data['data'])
        return await self._repository.create(event_data)

    async def get_events(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        event_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[LifeEvent]:
        """Get life events with filtering"""
        filters = {
            'start_date': start_date,
            'end_date': end_date,
            'event_type': event_type,
            'limit': limit,
            'offset': offset
        }
        return await self._repository.get_filtered(filters)

    def _validate_event_data(self, schema: dict, data: dict) -> None:
        """Validate event data against its type's schema"""
        try:
            jsonschema.validate(data, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(f"Invalid event data: {str(e)}")
```

## Key Responsibilities

1. **Data Validation**
   - JSON Schema validation for event types
   - Event data validation against type schemas
   - Input data sanitization and normalization

2. **Business Logic**
   - Event creation and retrieval logic
   - Temporal data management
   - Event type management

3. **Data Transformation**
   - Date/time handling and timezone conversion
   - Data format standardization
   - Response formatting

## Service Layer Patterns

### 1. Schema Validation

```python
def _validate_event_data(self, schema: dict, data: dict) -> None:
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(f"Invalid event data: {str(e)}")
```

### 2. Temporal Filtering

```python
async def get_events_by_timerange(
    self,
    start: datetime,
    end: datetime
) -> List[LifeEvent]:
    return await self._repository.get_by_timerange(start, end)
```

### 3. Event Type Management

```python
async def get_events_by_type(
    self,
    type_name: str,
    limit: int = 50
) -> List[LifeEvent]:
    event_type = await self._type_service.get_event_type_by_name(type_name)
    return await self._repository.get_by_type(event_type.id, limit)
```

## Integration Examples

### 1. Creating a Photo Event

```python
# Example of creating a photo event
photo_data = {
    "event_type_id": 1,  # photo type
    "data": {
        "photo_url": "https://example.com/photo.jpg",
        "location": {"lat": 37.7749, "lng": -122.4194},
        "caption": "Beautiful sunset"
    }
}

event = await life_event_service.create_event(photo_data)
```

### 2. Querying Exercise Events

```python
# Get today's exercise events
today = datetime.now().date()
exercises = await life_event_service.get_events(
    start_date=today,
    event_type="exercise",
    limit=10
)
```

## Error Handling

1. **Validation Errors**
   - Schema validation errors
   - Data format errors
   - Required field validation

2. **Business Logic Errors**
   - Invalid event types
   - Date range errors
   - Resource not found

3. **System Errors**
   - Database errors
   - External service errors
   - Timeout handling

## Testing Strategy

1. **Unit Tests**
   - Schema validation tests
   - Business logic tests
   - Error handling tests

2. **Integration Tests**
   - Repository integration
   - Event type validation
   - Temporal query tests

3. **Mock Examples**
```python
@pytest.mark.asyncio
async def test_create_event():
    # Mock dependencies
    event_repo = Mock(spec=LifeEventRepository)
    type_service = Mock(spec=EventTypeService)
    
    # Setup test data
    event_type = EventType(
        id=1,
        name="test",
        schema={"type": "object"}
    )
    type_service.get_event_type.return_value = event_type
    
    # Create service with mocks
    service = LifeEventService(event_repo, type_service)
    
    # Test event creation
    event_data = {"event_type_id": 1, "data": {}}
    await service.create_event(event_data)
    
    # Verify calls
    event_repo.create.assert_called_once_with(event_data)
``` 