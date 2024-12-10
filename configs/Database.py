from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from configs.Environment import get_environment_variables

# Initialize environment variables
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

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=env.DEBUG_MODE,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init() -> None:
    """Initialize database."""
    from models.BaseModel import Base

    Base.metadata.create_all(bind=engine)
