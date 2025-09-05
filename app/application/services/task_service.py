from uuid import UUID
from app.domain.unit_of_work import IUnitOfWork
from app.domain.entities.tasks import Task
from app.infrastructure.dtos.task_dtos import CreateTaskDto, UpdateTaskDto, TaskDto, TaskResponseDto
from app.infrastructure.common.paginated_results import CursorPaginationRequest, CursorPagedResult
from app.application.exceptions import TaskNotFound, ServiceException

class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    def create_task(self, task_dto: CreateTaskDto) -> TaskResponseDto:
        with self._uow as uow:
            task = Task(
                title=task_dto.title, 
                description=task_dto.description, 
                status=task_dto.status, 
                user_id=task_dto.user_id
            )
            saved_task = uow.tasks.create(task)
            uow.commit()
            return self._domain_to_response_dto(saved_task)

    def get_task_by_id(self, task_id: UUID, user_id: UUID) -> TaskResponseDto:
        with self._uow as uow:
            try:
                task = uow.tasks.get_by_id(task_id, user_id)
                if not task:
                    raise TaskNotFound()
                return self._domain_to_response_dto(task)
            except TaskNotFound:
                raise
            except Exception as e:
                raise ServiceException(f"Failed to get task: {str(e)}")
        
    def update_task(self, task_update_dto: UpdateTaskDto, user_id: UUID) -> TaskResponseDto:
        with self._uow as uow:
            try:
                task = uow.tasks.get_by_id(task_update_dto.id, user_id)
                if not task:
                    raise TaskNotFound()
                
                task.update_task(
                    task_update_dto.title, 
                    task_update_dto.description, 
                    task_update_dto.status
                )
                updated_task = uow.tasks.update(task)
                uow.commit()
                return self._domain_to_response_dto(updated_task)
            except TaskNotFound:
                raise
            except Exception as e:
                raise ServiceException(f"Failed to update task: {str(e)}")
        
    def delete_task(self, task_id: UUID, user_id: UUID) -> None:
        with self._uow as uow:
            try:
                task = uow.tasks.get_by_id(task_id, user_id)
                if not task:
                    raise TaskNotFound()
                uow.tasks.delete(task_id)
                uow.commit()
            except TaskNotFound:
                raise
            except Exception as e:
                raise ServiceException(f"Failed to delete task: {str(e)}")
        
    def get_all_tasks_paginated_by_cursor(self, user_id: UUID, pagination_request: CursorPaginationRequest) -> CursorPagedResult[TaskDto]:
        if not user_id:
            raise ServiceException("User ID is required")
        
        with self._uow as uow:
            return uow.tasks.get_all_paginated_by_cursor(user_id, pagination_request)

    def _domain_to_response_dto(self, task: Task) -> TaskResponseDto:
        return TaskResponseDto(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=task.user_id,
            created_at=task.creation_date,
            updated_at=task.updated_at
        ) 