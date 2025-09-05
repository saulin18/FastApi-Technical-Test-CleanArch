
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from uuid import UUID
from app.infrastructure.database import get_db
from app.infrastructure.common.paginated_results import (
    CursorPagedResult, 
    CursorPaginationRequest, 
    PaginationDirection
)
from app.application.services.task_service import TaskService
from app.infrastructure.dtos.task_dtos import TaskDto, CreateTaskDto, UpdateTaskDto, TaskResponseDto
from app.infrastructure.common.sql_alchemy_unit_of_work import SQLModelUnitOfWork
from app.presentation.exceptions.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("/", response_model=CursorPagedResult[TaskDto])
async def get_tasks_with_cursor_pagination(
    user_id: UUID,
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    page_size: int = Query(10, ge=1, le=50, description="Number of items per page"),
    direction: PaginationDirection = Query(PaginationDirection.FORWARD, description="Pagination direction"),
    db: Session = Depends(get_db)
):
    try:
        pagination_request = CursorPaginationRequest(
            cursor=cursor,
            page_size=page_size,
            direction=direction
        )
        
        uow = SQLModelUnitOfWork(lambda: db)
        service = TaskService(uow)
        result = service.get_all_tasks_paginated_by_cursor(user_id, pagination_request)
        
        return result
    except Exception as e:
        if "User ID is required" in str(e):
            raise ValidationException("User ID is required")
        raise ValidationException(f"Failed to get tasks: {str(e)}")


@router.post("/", response_model=TaskResponseDto)
async def create_task(
    task_dto: CreateTaskDto,
    db: Session = Depends(get_db)
):
   
    uow = SQLModelUnitOfWork(lambda: db)
    service = TaskService(uow)
    return service.create_task(task_dto)


@router.get("/{task_id}", response_model=TaskResponseDto)
async def get_task(
    task_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):
    uow = SQLModelUnitOfWork(lambda: db)
    service = TaskService(uow)
    try:
        return service.get_task_by_id(task_id, user_id)
    except Exception as e:
        if "Task not found" in str(e):
            raise NotFoundException("Task")
        raise ValidationException(f"Failed to get task: {str(e)}")


@router.put("/{task_id}", response_model=TaskResponseDto)
async def update_task(
    task_id: UUID,
    task_update_dto: UpdateTaskDto,
    user_id: UUID,
    db: Session = Depends(get_db)
):
    uow = SQLModelUnitOfWork(lambda: db)
    service = TaskService(uow)
    try:
        return service.update_task(task_update_dto, user_id)
    except Exception as e:
        if "Task not found" in str(e):
            raise NotFoundException("Task")
        raise ValidationException(f"Failed to update task: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):
    uow = SQLModelUnitOfWork(lambda: db)
    service = TaskService(uow)
    try:
        service.delete_task(task_id, user_id)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        if "Task not found" in str(e):
            raise NotFoundException("Task")
        raise ValidationException(f"Failed to delete task: {str(e)}")
