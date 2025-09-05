from sqlmodel import Session, select
from app.domain.repositories.itask_repository import ITaskRepository
from app.domain.entities.tasks import Task
from app.infrastructure.persistence.entities_configuration import Task as TaskEntity
from uuid import UUID
from typing import Optional, List
from app.infrastructure.dtos.task_dtos import TaskDto
from app.infrastructure.common.paginated_results import CursorPaginationRequest, CursorPagedResult, CursorPaginationHelper
from app.infrastructure.exceptions import TaskNotFound


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self, user_id: UUID) -> List[Task]:
        statement = select(TaskEntity).where(TaskEntity.user_id == user_id)
        task_entities = self._session.exec(statement).all()
        return [self._entity_to_domain(task_entity) for task_entity in task_entities]
   
    def get_all_paginated_by_cursor(self, user_id: UUID, pagination_request: CursorPaginationRequest) -> CursorPagedResult[TaskDto]:
        statement = select(TaskEntity).where(TaskEntity.user_id == user_id)
        
        statement = CursorPaginationHelper.build_cursor_query(
            statement,
            TaskEntity,
            key_selector="id",
            cursor=pagination_request.cursor,
            page_size=pagination_request.page_size,
            direction=pagination_request.direction
        )
        
        task_entities = self._session.exec(statement).all()
        task_dtos = [self._entity_to_dto(task_entity) for task_entity in task_entities]
        
        return CursorPaginationHelper.apply_cursor_pagination_to_query_result(
            items=task_dtos,
            key_selector="id",
            cursor=pagination_request.cursor,
            page_size=pagination_request.page_size,
            direction=pagination_request.direction
        )

    def get_by_id(self, id: UUID, user_id: UUID) -> Optional[Task]:
        statement = select(TaskEntity).where(
            TaskEntity.id == id, 
            TaskEntity.user_id == user_id
        )
        task_entity = self._session.exec(statement).first()
        return self._entity_to_domain(task_entity) if task_entity else None

    def create(self, task: Task) -> Task:
        task_entity = TaskEntity(
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=task.user_id
        )
        self._session.add(task_entity)
        self._session.commit()
        self._session.refresh(task_entity)
        return self._entity_to_domain(task_entity)

    def update(self, task: Task) -> Task:
        statement = select(TaskEntity).where(TaskEntity.id == task.id)
        task_entity = self._session.exec(statement).first()
        
        if task_entity:
            task_entity.title = task.title
            task_entity.description = task.description
            task_entity.status = task.status
            task_entity.updated_at = task.updated_at
            self._session.add(task_entity)
            self._session.commit()
            self._session.refresh(task_entity)
            return self._entity_to_domain(task_entity)
        else:
            raise TaskNotFound()
    

    def delete(self, id: UUID) -> None:
        statement = select(TaskEntity).where(TaskEntity.id == id)
        task_entity = self._session.exec(statement).first()
        if task_entity:
            self._session.delete(task_entity)
            self._session.commit()
        else:
            raise TaskNotFound()

    def _entity_to_domain(self, task_entity: TaskEntity) -> Task:
        task = Task(
            title=task_entity.title,
            description=task_entity.description,
            status=task_entity.status,
            user_id=task_entity.user_id
        )
        task.id = task_entity.id
        task.creation_date = task_entity.creation_date
        task.updated_at = task_entity.updated_at
        return task

    def _entity_to_dto(self, task_entity: TaskEntity) -> TaskDto:
        return TaskDto(
            id=task_entity.id,
            title=task_entity.title,
            description=task_entity.description,
            status=task_entity.status,
            user_id=task_entity.user_id,
            creation_date=task_entity.creation_date,
            updated_at=task_entity.updated_at
        )