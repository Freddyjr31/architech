from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from features.auth.repository.repository import AuthRepository
from features.auth.services.auth_service import AuthService
from features.auth.schemas.auth_schemas import UserLoginRequest

from schemas.schemas import ErrorResponse, TokenResponse
from core.logger import logger
from core import security
from core.database import get_db

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

def get_auth_repository(db: Annotated[Session, Depends(get_db)]):
    return AuthRepository(db)

def get_auth_service(repository: Annotated[AuthRepository, Depends(get_auth_repository)]):
    return AuthService(repository)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={401: {"model": ErrorResponse}},
    )
def login_user(
    payload: UserLoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
    ):
    """
    Endpoint para autenticar a un usuario y generar un token JWT.
    """
    
    logger.info(f"Intento de inicio de sesión para usuario: {payload.username}")
    
    #* verifico si el usuario existe
    user_auth = service.authenticate_user(payload)

    #* Genero el token de acceso JWT para el usuario autenticado
    token = security.create_access_token(data=user_auth)
    logger.info(f"Inicio de sesión exitoso para usuario: {payload.username}. Token generado.")
    
    return TokenResponse(access_token=token)