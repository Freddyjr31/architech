

from features.projects.services.project_services import ProjectService
from features.projects.repository.project_repository_impl import ProjectRepositoryImpl
from features.projects.repository.project_repository_interface import ProjectRepositoryInterface
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db


def get_project_repository(
    db: Session = Depends(get_db)
    ) -> ProjectRepositoryInterface:
    return ProjectRepositoryImpl(db)

def get_project_service(
    project_repository: ProjectRepositoryInterface = Depends(get_project_repository)
    ) -> ProjectService:
    return ProjectService(project_repository)