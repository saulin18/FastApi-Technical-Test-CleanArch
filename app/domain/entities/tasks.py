from uuid import UUID
from typing import Optional
from datetime import datetime
from app.domain.constants.TASK_STATUS import TaskStatus
import uuid

class Task():
    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    creation_date: datetime
    updated_at: datetime
    user_id: UUID
    
    def __init__(self, title: str, description: Optional[str], status: TaskStatus, user_id: UUID):
        self.id = uuid.uuid4()
        self.title = title
        self.description = description
        self.status = status
        self.creation_date = datetime.now()
        self.updated_at = datetime.now()
        self.user_id = user_id
        
    def update_task(self, title: str, description: Optional[str], status: TaskStatus):
        self.title = title
        self.description = description
        self.status = status
        self.updated_at = datetime.now()
        
    def mark_as_pending(self):
        self.status = TaskStatus.PENDING
        self.updated_at = datetime.now()
        
    def mark_as_completed(self):
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now()