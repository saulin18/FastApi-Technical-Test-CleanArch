
from abc import ABC, abstractmethod

class IUnitOfWork(ABC):
    """Unit of Work interface for transaction management."""
    
    @abstractmethod
    def commit(self):
        """Commit the current transaction."""
        pass
    
    @abstractmethod
    def rollback(self):
        """Rollback the current transaction."""
        pass
    
    