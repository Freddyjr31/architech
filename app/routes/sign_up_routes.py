# from typing import Annotated

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from core.database import get_db
# from core.logger import logger
# from features.sign_up.exceptions import SignUpError
# from features.sign_up.schemas.sign_up_schemas import UserRegisterRequest, UserRegisterResponse
# from features.sign_up.services.sign_up_service import register_user
# from schemas.schemas import ErrorResponse

# router = APIRouter(
#     prefix="/api/v1/register",
#     tags=["Sign Up"],
# )

# @router.post(
#     "/sign-up",
#     response_model=UserRegisterResponse,
#     status_code=status.HTTP_201_CREATED,
#     responses={400: {"model": ErrorResponse}},
#     )
# async def sign_up_user(user: UserRegisterRequest, db: Annotated[Session, Depends(get_db)]):
#     """
#     Endpoint para registrar un nuevo usuario.
#     """

#     try:
#         new_user = register_user(user, db)

#         return UserRegisterResponse(
#             id=new_user.id,
#             username=new_user.username,
#             email=new_user.email,
#             created_at=new_user.created_at,
#             message="Usuario registrado exitosamente."
#         )

#     except SignUpError:
#         db.rollback()
#         raise

#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error inesperado al registrar usuario: {e}", exc_info=True)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al registrar el usuario.")