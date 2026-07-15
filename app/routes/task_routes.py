from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from features.tasks.schemas.tasks_schemas import CreateTaskRequest, CreateTaskResponse, DeleteTaskRequest
from schemas.schemas import ErrorResponse
from core.logger import logger
from core.database import get_db
from core import security, dependencies

router = APIRouter(
    prefix="/api/v1/task",
    tags=["Task"],
    dependencies=[Depends(dependencies.get_current_user)]
)

@router.post(
    "/create-task",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorResponse}},
    )
async def create_task(payload: CreateTaskRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint para crear una tarea
    """

    logger.info(f"Intento de crear tarea para usuario: {payload.owner_id}")
    
    return {"message":"tarea creada con éxito"}


@router.delete(
    "/delete-task/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"model": ErrorResponse}}
    # response_model=
)
def delete_task(id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint para eliminar una tarea o lista de tareas
    """
    
    return Response(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Tarea eliminada con éxito"})