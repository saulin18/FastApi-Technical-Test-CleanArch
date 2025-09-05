from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserDto(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class SignUpDto(BaseModel):
    name: str
    email: str
    password: str


class SignInDto(BaseModel):
    email: str
    password: str


class TokenDto(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenDto(BaseModel):
    refresh_token: str


class RefreshTokenResponseDto(BaseModel):
    access_token: str
    token_type: str