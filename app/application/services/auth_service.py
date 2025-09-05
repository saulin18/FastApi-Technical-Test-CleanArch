from app.domain.unit_of_work import IUnitOfWork
from app.infrastructure.dtos.user_dtos import SignUpDto, SignInDto, RefreshTokenResponseDto, UserDto
from app.infrastructure.common.auth_service import AuthService as InfrastructureAuthService
from uuid import UUID
from app.application.exceptions import AuthenticationFailed, InvalidCredentials, ServiceException
from sqlmodel import Session


class AuthService:
    def __init__(self, uow: IUnitOfWork, session: Session):
        self._uow = uow
        self._infrastructure_auth_service = InfrastructureAuthService(session)

    def sign_up(self, user_sign_up_request: SignUpDto) -> dict:
        with self._uow as uow:
            try:
                saved_user = uow.users.sign_up(
                    user_sign_up_request.name,
                    user_sign_up_request.email,
                    user_sign_up_request.password
                )
                uow.commit()
                
                user_dto = UserDto(
                    id=saved_user.id,
                    name=saved_user.name,
                    email=saved_user.email,
                    created_at=saved_user.created_at,
                    updated_at=saved_user.updated_at
                )
                tokens = self._infrastructure_auth_service.create_tokens_for_user(user_dto)
                
                return tokens
            except Exception as e:
                raise ServiceException(f"Sign up failed: {str(e)}")
            
    def sign_in(self, user_sign_in_request: SignInDto) -> dict:
        with self._uow as uow:
            try:
                user = uow.users.sign_in(
                    user_sign_in_request.email,
                    user_sign_in_request.password
                )
                
               
                user_dto = UserDto(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                tokens = self._infrastructure_auth_service.create_tokens_for_user(user_dto)
                
                return tokens
            except InvalidCredentials:
                raise
            except Exception as e:
                raise ServiceException(f"Sign in failed: {str(e)}")
    
    def refresh_access_token(self, refresh_token: str) -> RefreshTokenResponseDto:
        try:
            tokens = self._infrastructure_auth_service.refresh_access_token(refresh_token)
            return RefreshTokenResponseDto(
                access_token=tokens["access_token"],
                token_type=tokens["token_type"]
            )
        except Exception as e:
            raise AuthenticationFailed(f"Token refresh failed: {str(e)}")
            
    def revoke_refresh_token(self, refresh_token: str) -> bool:
        try:
            return self._infrastructure_auth_service.revoke_refresh_token(refresh_token)
        except Exception as e:
            raise ServiceException(f"Token revocation failed: {str(e)}")
        
    def revoke_all_user_tokens(self, user_id: UUID) -> None:
        try:
            self._infrastructure_auth_service.revoke_all_user_tokens(user_id)
        except Exception as e:
            raise ServiceException(f"Token revocation failed: {str(e)}")
    
    def create_tokens_for_user(self, user_dto: UserDto) -> dict:
       
        return self._infrastructure_auth_service.create_tokens_for_user(user_dto)