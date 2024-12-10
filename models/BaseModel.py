"""Base model for all database entities."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta


class ModelBase:
    """Base class for all models."""

    class Config:
        """SQLAlchemy model configuration."""

        arbitrary_types_allowed = True
        from_attributes = True


Base = declarative_base(cls=ModelBase)

__all__ = ["Base"]
