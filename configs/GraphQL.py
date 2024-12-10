from typing import Dict, Any
from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db


async def get_graphql_context(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Create GraphQL context with database session."""
    return {"db": db}
