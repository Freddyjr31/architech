from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from features.proyects.schemas.proyect_schemas import DeleteProyectRequest, CreateProyectRequest, CreateProyectResponse
from schemas.schemas import ErrorResponse
from core.logger import logger
from core.database import get_db
from core import security

router = APIRouter(
    prefix="/api/v1/proyect",
    tags=["Proyects"],
)

@router.post(
    "/create-project",
    response_model=CreateProyectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorResponse}},
    )
async def create_proyect(payload: CreateProyectRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint para crear un proyecto
    """
    
    logger.info(f"Intento de inicio de sesión para usuario: {payload.username}")
    
    return {'message':'proyecto creado!'}

@router.delete(
    "/delete-project/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"model": ErrorResponse}}
)
def delete_proyect(id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint para eliminar un proyecto
    """
    
    return Response(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Proyecto eliminado con éxito"})