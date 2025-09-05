from pydantic import BaseModel
from typing import Optional
from app.domain.constants.TASK_STATUS import TaskStatus
from uuid import UUID
from datetime import datetime

class CreateTaskDto(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    user_id: UUID

class UpdateTaskDto(BaseModel):
    id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    updated_at: datetime

class TaskDto(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    user_id: UUID

class TaskResponseDto(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    user_id: UUID
    created_at: datetime
    updated_at: datetime