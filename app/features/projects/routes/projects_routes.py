from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from core import dependencies
from core.logger import logger

from features.projects.schemas.project_schemas import CreateProjectRequest, CreateProjectResponse
from features.projects.services.project_services import (
    ProjectService
)
from schemas.schemas import ErrorResponse

from features.projects.dependencies import get_project_service

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
    dependencies=[Depends(dependencies.get_current_user)]
)

@router.post(
    "/create-project",
    response_model=CreateProjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorResponse}},
    )
def create_Project(
    payload: CreateProjectRequest,
    service: Annotated[ProjectService, Depends(get_project_service)],
    current_user: dependencies.CurrentUser,
):
    """
    Endpoint para crear un Projecto
    """

    logger.info(f"Intento de crear Projecto nombre {payload.title}")
    owner_id: int = current_user["user_id"]

    project = service.create_project_service(payload, owner_id)

    logger.info(f"Projecto creado exitosamente: {project.id} - {project.title}")

    return CreateProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        created_at=project.created_at,
        message="¡Proyecto creado exitosamente!",
    )

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
)
def delete_Project(
    id: int,
    current_user: dependencies.CurrentUser,
    service: Annotated[ProjectService, Depends(get_project_service)]
    ):
    """
    Endpoint para eliminar un Projecto
    """
    
    current_user_id: int = current_user["user_id"]
    service.delete_project_service(id, current_user_id)
    logger.info(f"Projecto eliminado con éxito: {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
