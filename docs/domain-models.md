# Domain Models

## Overview

The domain models represent the core business entities in our application. They are located in the `models/` directory and are designed to be independent of any external frameworks or libraries.

## Core Entities

### 1. Book Model

```python
# models/BookModel.py
class BookModel(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    authors = relationship("AuthorModel", secondary="book_author_association")
```

The Book entity represents a book in our system with:
- Unique identifier
- Title and description
- Many-to-many relationship with authors

### 2. Author Model

```python
# models/AuthorModel.py
class AuthorModel(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    books = relationship("BookModel", secondary="book_author_association")
```

The Author entity represents an author with:
- Unique identifier
- Name
- Many-to-many relationship with books

### 3. Book-Author Association

```python
# models/BookAuthorAssociation.py
class BookAuthorAssociation(Base):
    __tablename__ = "book_author_association"
    
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
```

This model manages the many-to-many relationship between books and authors.

## Domain Model Characteristics

1. **Pure Business Logic**
   - Models contain only business rules and logic
   - No dependencies on external frameworks
   - No knowledge of persistence mechanisms

2. **Relationship Management**
   - Clear definition of entity relationships
   - Proper encapsulation of data
   - Bidirectional navigation capabilities

3. **Validation Rules**
   - Built-in data validation
   - Business rule enforcement
   - Type safety

## Base Model

```python
# models/BaseModel.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init():
    """Initialize the models"""
    Base.metadata.create_all(bind=engine)
```

The Base model:
- Provides common functionality
- Handles database initialization
- Manages model metadata

## Usage in Clean Architecture

The domain models are:
1. **Central to the Architecture**
   - Core business rules reside here
   - Other layers depend on these models
   - Changes here affect the entire system

2. **Framework Independent**
   - No SQLAlchemy-specific logic in business rules
   - Can be used with any persistence mechanism
   - Easily testable in isolation

3. **Single Responsibility**
   - Each model represents one business concept
   - Clear and focused responsibilities
   - Easy to maintain and modify 