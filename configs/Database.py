from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from configs.Environment import get_environment_variables

env = get_environment_variables()

# Construct Database URL
DATABASE_URL = (
    f"{env.DATABASE_DIALECT}://"
    f"{env.DATABASE_USERNAME}:"
    f"{env.DATABASE_PASSWORD}@"
    f"{env.DATABASE_HOSTNAME}:"
    f"{env.DATABASE_PORT}/"
    f"{env.DATABASE_NAME}"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=env.DEBUG_MODE,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Create base class for declarative models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init() -> None:
    """Initialize database models."""
    # Import all models to ensure they're registered
    from models.EventTypeModel import (
        EventType,
    )  # noqa: F401
    from models.LifeEventModel import (
        LifeEvent,
    )  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)
