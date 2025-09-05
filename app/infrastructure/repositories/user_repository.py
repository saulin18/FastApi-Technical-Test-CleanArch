from sqlmodel import Session, select
from app.domain.repositories.iuser_repository import IUserRepository
from app.domain.entities.users import User
from app.infrastructure.persistence.entities_configuration import User as UserEntity
from app.infrastructure.dtos.user_dtos import UserDto
from uuid import UUID
from typing import Optional
import hashlib
from app.infrastructure.exceptions import UserAlreadyExists, InvalidCredentials

class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: UUID) -> Optional[User]:
        user_entity = self._session.get(UserEntity, id)
        return self._entity_to_domain(user_entity) if user_entity else None

    def create(self, user: User) -> User:
        user_entity = UserEntity(
            name=user.name,
            email=user.email,
            password=self._hash_password(user.password)
        )
        self._session.add(user_entity)
        self._session.commit()
        self._session.refresh(user_entity)
        return self._entity_to_domain(user_entity)

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(UserEntity).where(UserEntity.email == email)
        user_entity = self._session.exec(statement).first()
        return self._entity_to_domain(user_entity) if user_entity else None

    def sign_up(self, name: str, email: str, password: str) -> User:
        existing_user = self.get_by_email(email)
        if existing_user:
            raise UserAlreadyExists()
        
        
        user_entity = UserEntity(
            name=name,
            email=email,
            password=self._hash_password(password)
        )
        self._session.add(user_entity)
        self._session.commit()
        self._session.refresh(user_entity)
        return self._entity_to_domain(user_entity)

    def sign_in(self, email: str, password: str) -> Optional[User]:
        user_entity = self.get_by_email(email)
        if not user_entity:
            raise InvalidCredentials("Invalid email or password")
        
        if not self._verify_password(password, user_entity.password):
            raise InvalidCredentials("Invalid email or password")
        
        return user_entity

    def _entity_to_domain(self, user_entity: UserEntity) -> User:
        return User(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            password=user_entity.password,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )

    def _entity_to_dto(self, user_entity: UserEntity) -> UserDto:
        return UserDto(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )

    def _entity_to_dto_from_domain(self, user: User) -> UserDto:
        return UserDto(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self._hash_password(password) == hashed_password
