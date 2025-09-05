
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from uuid import UUID, uuid4
from app.domain.constants.TASK_STATUS import TaskStatus


class User(SQLModel, table=True):
    
    __tablename__ = "users"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=255, unique=True, index=True)
    password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
 
    tasks: List["Task"] = Relationship(back_populates="user")
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):

    __tablename__ = "tasks"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(max_length=1000, default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID = Field(foreign_key="users.id", index=True)
 
    user: User = Relationship(back_populates="tasks")


class RefreshToken(SQLModel, table=True):
   
    __tablename__ = "refresh_tokens"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    token: str = Field(max_length=500, unique=True, index=True)
    expires_at: datetime
    is_revoked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID = Field(foreign_key="users.id", index=True)
    
    user: User = Relationship(back_populates="refresh_tokens")
