from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.schemas import ErrorResponse, TokenResponse
from core.logger import logger
from core.database import get_db
from features.auth.schemas.auth_schemas import UserLoginRequest
from features.auth.services.auth import verify_user
from core import security

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={401: {"model": ErrorResponse}},
    )
async def login_user(payload: UserLoginRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint para autenticar a un usuario y generar un token JWT.
    """
    
    logger.info(f"Intento de inicio de sesión para usuario: {payload.username}")
    
    #* verifico si el usuario existe
    existing_user = verify_user(payload.username, db)
    
    if not existing_user or not security.verify_password(payload.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas. Usuario o contraseña incorrectos."
            )

    #* Genero el token de acceso JWT para el usuario autenticado
    token = security.create_access_token(data={"sub": existing_user.username})
    logger.info(f"Inicio de sesión exitoso para usuario: {payload.username}. Token generado.")
    
    return TokenResponse(access_token=token)