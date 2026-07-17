from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from core import dependencies
from core.database import get_db
from core.logger import logger
from features.projects.exceptions import ProjectError
from features.projects.schemas.project_schemas import CreateProjectRequest, CreateProjectResponse
from features.projects.services.project_services import (
    create_project_service,
    delete_project_service
)
from schemas.schemas import ErrorResponse

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
async def create_Project(
    payload: CreateProjectRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: dependencies.CurrentUser,
):
    """
    Endpoint para crear un Projecto
    """

    logger.info(f"Intento de crear Projecto nombre {payload.title}")
    owner_id: int = current_user["user_id"]

    try:
        project = create_project_service(payload, owner_id, db)

        logger.info(f"Projecto creado exitosamente: {project.id} - {project.title}")

        return CreateProjectResponse(
            id=project.id,
            title=project.title,
            description=project.description,
            created_at=project.created_at,
            message="¡Proyecto creado exitosamente!",
        )

    except ProjectError:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear Projecto: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el Projecto.")


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
    db: Annotated[Session, Depends(get_db)],
    current_user: dependencies.CurrentUser
    ):
    """
    Endpoint para eliminar un Projecto
    """
    
    current_user_id: int = current_user["user_id"]
    delete_project_service(id, current_user_id, db)
    logger.info(f"Projecto eliminado con éxito: {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
