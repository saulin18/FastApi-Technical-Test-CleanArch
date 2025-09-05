import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from app.domain.entities.users import User
from app.infrastructure.persistence.entities_configuration import RefreshToken
from sqlmodel import Session
import hashlib
from app.core.config import settings
from app.infrastructure.dtos.user_dtos import UserDto
from app.infrastructure.persistence.entities_configuration import User as UserEntity
from sqlmodel import select, update
from app.infrastructure.exceptions import InvalidToken, UserNotFound

class AuthService:
    def __init__(self, session: Session):
        self._session = session
        self._secret_key = settings.jwt_secret_key
        self._algorithm = "HS256"
        self._access_token_expire_minutes = settings.access_token_expire_minutes
        self._refresh_token_expire_days = settings.refresh_token_expire_days

    def create_access_token(self, data: Dict[str, Any], expires_time: Optional[timedelta] = None) -> str:
       
        to_encode = data.copy()
        if expires_time:
            expire = datetime.now(timezone.utc) + expires_time
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def create_refresh_token(self, user_id: UUID) -> str:
       
        
        refresh_token_value = str(uuid4())
        
        
        hashed_token = hashlib.sha256(refresh_token_value.encode()).hexdigest()
        
        
        expires_at = datetime.now(timezone.utc) + timedelta(days=self._refresh_token_expire_days)
        
        
        refresh_token_entity = RefreshToken(
            token=hashed_token,
            expires_at=expires_at,
            user_id=user_id
        )
        
        self._session.add(refresh_token_entity)
        self._session.commit()
        
        return refresh_token_value

    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
       
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except jwt.PyJWTError:
            return None

    def verify_refresh_token(self, refresh_token: str) -> Optional[RefreshToken]:
       
        hashed_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        
        
        statement = select(RefreshToken).where(
            RefreshToken.token == hashed_token,
            RefreshToken.is_revoked is False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        )
        
        refresh_token_entity = self._session.exec(statement).first()
        return refresh_token_entity

    def revoke_refresh_token(self, refresh_token: str) -> bool:
       
        refresh_token_entity = self.verify_refresh_token(refresh_token)
        if refresh_token_entity:
            refresh_token_entity.is_revoked = True
            self._session.commit()
            return True
        raise InvalidToken("Invalid refresh token")

    def revoke_all_user_tokens(self, user_id: UUID) -> None:
       
        
        statement = update(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked is False
        ).values(is_revoked=True)
        
        self._session.exec(statement)
        self._session.commit()

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
       
        statement = select(UserEntity).where(UserEntity.email == email)
        user_entity = self._session.exec(statement).first()
        
        if not user_entity:
            return None
        
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user_entity.password != hashed_password:
            return None
        
        return User(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            password=user_entity.password,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )

    def create_tokens_for_user(self, user_dto: UserDto) -> Dict[str, str]:
       
        access_token_data = {
            "sub": str(user_dto.id),
            "email": user_dto.email,
            "name": user_dto.name
        }
        access_token = self.create_access_token(access_token_data)
        
        
        refresh_token = self.create_refresh_token(user_dto.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
       
        refresh_token_entity = self.verify_refresh_token(refresh_token)
        if not refresh_token_entity:
            raise InvalidToken("Invalid refresh token")
        

        user_entity = self._session.get(UserEntity, refresh_token_entity.user_id)
        if not user_entity:
            raise UserNotFound()
        
        
        user = User(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            password=user_entity.password,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )
        
        
        access_token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name
        }
        access_token = self.create_access_token(access_token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
