from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.schemas import ErrorResponse
from core.database import get_db
from features.sign_up.schemas.sign_up_schemas import UserRegisterRequest, UserRegisterResponse
from features.sign_up.services.sign_up_service import register_user

router = APIRouter(
    prefix="/api/v1/register",
    tags=["Sign Up"],
)

@router.post(
    "/sign-up",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}},
    )
async def sign_up_user(user: UserRegisterRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint para registrar un nuevo usuario.
    """
    
    new_user = register_user(user, db)
    
    if new_user:
        return UserRegisterResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            created_at=new_user.created_at,
            message="Usuario registrado exitosamente."
        )

    return new_user