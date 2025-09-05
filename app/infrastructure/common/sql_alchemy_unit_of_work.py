
from app.domain.unit_of_work import IUnitOfWork
from app.infrastructure.repositories.task_repository import TaskRepository
from app.infrastructure.repositories.user_repository import UserRepository


class SQLModelUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.tasks = TaskRepository(self._session)
        self.users = UserRepository(self._session)
        return self

    def __exit__(self, *args):
        self.rollback()
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()