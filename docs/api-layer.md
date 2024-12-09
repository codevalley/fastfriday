# API Layer Documentation

## Overview

The API layer serves as the interface between the external world and our application's business logic. This project implements both REST and GraphQL APIs, providing flexibility in how clients can interact with the system.

## REST API Implementation

### Router Structure

```python
# routers/v1/BookRouter.py
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.post("/")
async def create_book(
    book_data: BookCreate,
    service: BookService = Depends(get_book_service)
) -> Book:
    return await service.create_book(book_data.dict())

@router.get("/{book_id}")
async def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
) -> Book:
    return await service.get_book(book_id)
```

### Key Features

1. **Versioning**
   - API versioning through URL prefixes
   - Separate routers for different versions
   - Easy to maintain backward compatibility

2. **Dependency Injection**
   - Services injected via FastAPI's dependency system
   - Clean separation of concerns
   - Easy to test and mock dependencies

3. **Request/Response Models**
   - Pydantic models for validation
   - Clear API contracts
   - Automatic OpenAPI documentation

## GraphQL API Implementation

### Schema Definition

```python
# schemas/graphql/Query.py
import strawberry
from typing import List

@strawberry.type
class Query:
    @strawberry.field
    async def books(self) -> List[Book]:
        return await book_service.list_books()

    @strawberry.field
    async def book(self, id: int) -> Book:
        return await book_service.get_book(id)
```

### Mutations

```python
# schemas/graphql/Mutation.py
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_book(self, input: BookInput) -> Book:
        return await book_service.create_book(input.to_dict())
```

## API Features

1. **Dual API Support**
   - REST endpoints for traditional access
   - GraphQL for flexible queries
   - Consistent business logic across both

2. **Documentation**
   - OpenAPI (Swagger) for REST
   - GraphQL Playground
   - Auto-generated documentation

3. **Error Handling**
   - Consistent error responses
   - HTTP status codes for REST
   - GraphQL error types

## Implementation Details

### REST Endpoints

1. **Books API**
   ```
   POST   /api/v1/books          # Create book
   GET    /api/v1/books          # List books
   GET    /api/v1/books/{id}     # Get book
   PUT    /api/v1/books/{id}     # Update book
   DELETE /api/v1/books/{id}     # Delete book
   ```

2. **Authors API**
   ```
   POST   /api/v1/authors        # Create author
   GET    /api/v1/authors        # List authors
   GET    /api/v1/authors/{id}   # Get author
   PUT    /api/v1/authors/{id}   # Update author
   DELETE /api/v1/authors/{id}   # Delete author
   ```

### GraphQL Operations

1. **Queries**
   ```graphql
   query {
     books {
       id
       title
       authors {
         name
       }
     }
   }
   ```

2. **Mutations**
   ```graphql
   mutation {
     createBook(input: {
       title: "New Book"
       description: "Description"
     }) {
       id
       title
     }
   }
   ```

## Clean Architecture Integration

1. **Interface Adapters**
   - Converts between API and domain models
   - Handles HTTP/GraphQL specific logic
   - Maintains clean architecture boundaries

2. **Dependency Flow**
   - API layer depends on services
   - No direct database access
   - Follows dependency rule

3. **Validation**
   - Input validation at API level
   - Business validation in services
   - Clear separation of concerns 