from app.domain.entities.users import User
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

class IUserRepository(ABC):
    """User repository interface."""
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[User]:
        """Get user by id."""
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    def sign_up(self, name: str, email: str, password: str) -> User:
        """Sign up a new user."""
        pass
    
    @abstractmethod
    def sign_in(self, email: str, password: str) -> Optional[User]:
        """Sign in user with email and password."""
        pass
    
   