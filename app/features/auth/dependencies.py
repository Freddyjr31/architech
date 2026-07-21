from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from features.auth.repository.auth_repository_impl import AuthRepositoryImpl
from features.auth.repository.auth_repository_interface import AuthRepositoryInterface
from core.database import get_db
from features.auth.services.auth_service import AuthService


#? ---- Inyeccion de dependencias ----

def get_auth_repository(
    db: Annotated[Session, Depends(get_db)]
    ) -> AuthRepositoryInterface:
    return AuthRepositoryImpl(db)

def get_auth_service(
    repository: Annotated[AuthRepositoryInterface, Depends(get_auth_repository)]
    ) -> AuthService:
    return AuthService(repository)