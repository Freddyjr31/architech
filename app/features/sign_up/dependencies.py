from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from core.database import get_db

from features.sign_up.repository.signup_repository_impl import SignUpRepositoryImpl
from features.sign_up.repository.signup_repository_interface import SignUpRepositoryInterface
from features.sign_up.services.sign_up_service import SignUpService

def get_signup_repository(
    db: Annotated[Session, Depends(get_db)]
    ) -> SignUpRepositoryInterface:
    return SignUpRepositoryImpl(db)

def get_signup_service(
    signup_repository: Annotated[SignUpRepositoryInterface, Depends(get_signup_repository)]
    ) -> SignUpService:
    return SignUpService(signup_repository)