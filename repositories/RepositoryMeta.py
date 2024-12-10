from abc import abstractmethod
from typing import (
    Generic,
    List,
    TypeVar,
    Optional,
    Any,
    Dict,
)

# Type definition for Model
M = TypeVar("M")

# Type definition for Unique Id
K = TypeVar("K")


#################################
# Abstract Class for Repository #
#################################
class RepositoryMeta(Generic[M, K]):
    """Abstract base class for repositories."""

    # Create a new instance of the Model
    @abstractmethod
    def create(self, instance: M) -> M:
        """Create a new instance of the Model."""
        pass

    # Delete an existing instance of the Model
    @abstractmethod
    def delete(self, id: K) -> None:
        """Delete an existing instance of the Model."""
        pass

    # Fetch an existing instance of the Model by it's unique Id
    @abstractmethod
    def get(self, id: K) -> Optional[M]:
        """Get an existing instance of the Model by its unique Id."""
        pass

    # Lists all existing instance of the Model
    @abstractmethod
    def list(
        self,
        limit: Optional[int] = None,
        start: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[M]:
        """Get all instances of the Model with optional filtering."""
        pass

    # Updates an existing instance of the Model
    @abstractmethod
    def update(self, id: K, instance: M) -> M:
        """Update an existing instance of the Model."""
        pass
