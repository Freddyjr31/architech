from typing import Annotated
from fastapi import APIRouter, Depends, status

from core.logger import logger
from schemas.schemas import ErrorResponse

from features.sign_up.schemas.sign_up_schemas import UserRegisterRequest, UserRegisterResponse
from features.sign_up.dependencies import get_signup_service
from features.sign_up.services.sign_up_service import SignUpService

router = APIRouter(
    prefix="/api/v1/register",
    tags=["Sign Up"],
)

@router.post(
    "/",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}},
    )
def sign_up_user(
    user: UserRegisterRequest,
    service: Annotated[SignUpService, Depends(get_signup_service)]
    ):
    """
    Endpoint para registrar un nuevo usuario.
    """

    new_user = service.register_user(user)
    logger.info(f"Usuario registrado exitosamente: {new_user.id} - {new_user.username}")

    return UserRegisterResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=new_user.created_at,
        message="Usuario registrado exitosamente."
    )
