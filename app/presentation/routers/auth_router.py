from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.application.services.auth_service import AuthService
from app.infrastructure.database import get_db
from app.infrastructure.dtos.user_dtos import (
    SignUpDto, SignInDto, TokenDto, RefreshTokenDto, 
    RefreshTokenResponseDto
)
from app.presentation.exceptions.exceptions import AuthenticationException, ValidationException, ConflictResourceException
from app.infrastructure.common.sql_alchemy_unit_of_work import SQLModelUnitOfWork

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

def get_auth_service(session: Session = Depends(get_db)) -> AuthService:
    uow = SQLModelUnitOfWork(lambda: session)
    return AuthService(uow, session)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
   
    token = credentials.credentials
    payload = auth_service._infrastructure_auth_service.verify_access_token(token)
    if payload is None:
        raise AuthenticationException
    return payload

@router.post("/signup", response_model=TokenDto)
def sign_up(
    sign_up_dto: SignUpDto,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = auth_service.sign_up(sign_up_dto)
        return TokenDto(**tokens)
    
    except Exception as e:
        if "already exists" in str(e):
            raise ConflictResourceException("User")
        raise ValidationException(f"Sign up failed: {str(e)}")

@router.post("/signin", response_model=TokenDto)
def sign_in(
    sign_in_dto: SignInDto,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = auth_service.sign_in(sign_in_dto)
        return TokenDto(**tokens)
    except Exception as e:
        if "Invalid credentials" in str(e) or "Authentication failed" in str(e):
            raise AuthenticationException("Invalid email or password")
        raise ValidationException(f"Sign in failed: {str(e)}")

@router.post("/refresh", response_model=RefreshTokenResponseDto)
def refresh_token(
    refresh_dto: RefreshTokenDto,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.refresh_access_token(refresh_dto.refresh_token)
    except Exception as e:
        if "Invalid token" in str(e) or "Authentication failed" in str(e):
            raise AuthenticationException("Invalid refresh token")
        raise ValidationException(f"Token refresh failed: {str(e)}")

@router.post("/logout")
def logout(
    refresh_dto: RefreshTokenDto,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        auth_service.revoke_refresh_token(refresh_dto.refresh_token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        if "Invalid token" in str(e):
            raise AuthenticationException("Invalid refresh token")
        raise ValidationException(f"Logout failed: {str(e)}")