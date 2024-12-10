"""Base model for all database entities."""

from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base class
Base = declarative_base()


class BaseModel(Base):
    """Base model class with common functionality."""

    __abstract__ = True
