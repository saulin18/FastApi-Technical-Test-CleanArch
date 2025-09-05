from app.domain.entities.tasks import Task
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.infrastructure.common.paginated_results import CursorPaginationRequest, CursorPagedResult
from app.infrastructure.dtos.task_dtos import TaskDto

class ITaskRepository(ABC):
    """Task repository interface."""
    
    @abstractmethod
    def get_all(self, user_id: UUID) -> List[Task]:
        """Get all tasks for a user."""
        pass
    
    @abstractmethod
    def get_all_paginated_by_cursor(self, user_id: UUID, pagination_request: CursorPaginationRequest) -> CursorPagedResult[TaskDto]:
        """Get all tasks paginated by cursor efficiently."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID, user_id: UUID) -> Optional[Task]:
        """Get task by id and user_id."""
        pass
    
    @abstractmethod
    def create(self, task: Task) -> Task:  
        """Create a new task."""
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        """Update an existing task."""
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Delete a task by id."""
        pass
        