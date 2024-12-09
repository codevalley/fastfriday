# Clean Architecture Implementation

## Overview

This project implements the Clean Architecture (also known as Hexagonal Architecture) pattern, which emphasizes separation of concerns and dependency inversion. The architecture is organized in concentric circles, with the domain layer at the center and external concerns at the outer layers.

## Architectural Principles

1. **Independence of Frameworks**: The business logic is isolated from the delivery mechanism (FastAPI) and external frameworks.
2. **Testability**: The architecture makes the system highly testable by isolating components.
3. **Independence of UI**: The system works without the need to know about the final UI (REST or GraphQL).
4. **Independence of Database**: The business rules don't know about the persistence mechanism.
5. **Independence of External Agency**: Business rules don't know about the outside world.

## Layer Details

### 1. Domain Layer (Inner Circle)

Located in `models/`, this layer contains:
- Core business entities (Book, Author)
- Business rules and logic
- Interface definitions
- No dependencies on outer layers

Example:
```python
# models/BookModel.py - Core domain entity
class BookModel(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    # ... other fields
```

### 2. Application Layer

Located in `services/`, this layer:
- Implements use cases
- Orchestrates the flow of data
- Contains business logic
- Depends only on the domain layer

Example:
```python
# services/BookService.py - Application service
class BookService:
    def __init__(self, repository: BookRepository):
        self._repository = repository
    
    def create_book(self, book_data: dict) -> BookModel:
        # Business logic implementation
```

### 3. Interface Adapters

Located in `repositories/` and `routers/`, this layer:
- Converts data between formats
- Implements repository interfaces
- Handles HTTP requests/responses
- Contains controllers and presenters

### 4. External Interfaces

Located in various outer layer directories:
- REST API endpoints (`routers/`)
- GraphQL schema (`schemas/graphql/`)
- Database configurations (`configs/`)
- External service integrations

## Dependency Flow

The dependencies flow from the outer layers inward:
```
External Layer (REST/GraphQL) → Interface Adapters → Application Services → Domain Model
```

## Key Implementation Patterns

1. **Dependency Injection**
   - Used throughout the application
   - Facilitates testing and loose coupling
   - Implemented using FastAPI's dependency injection system

2. **Repository Pattern**
   - Abstracts data persistence
   - Allows swapping of data sources
   - Implements CRUD operations

3. **DTO Pattern**
   - Separates domain models from API contracts
   - Handles data validation
   - Implements using Pydantic models

## Benefits of This Architecture

1. **Maintainability**: Changes in external layers don't affect the business logic
2. **Testability**: Each layer can be tested in isolation
3. **Flexibility**: Easy to change frameworks, databases, or UI
4. **Scalability**: Clear boundaries make it easier to scale components independently 