from pydantic import BaseModel, Field
from datetime import datetime

class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    project_id: int = Field(..., description="ID del proyecto al que pertenece la tarea")
    date_init: datetime = Field(..., description="Fecha de inicio de la tarea")
    date_finish: datetime = Field(..., description="Fecha de fin de la tarea")
    owner_id: int = Field(..., description="ID del usuario que creo la tarea")
    assigned_id: int = Field(..., description="ID del usuario que se le asigno la tarea")

class CreateTaskResponse(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    created_at: datetime = Field(..., description="Fecha de creación del usuario")
    message: str = Field(..., description="Mensaje de éxito del registro")
    
class DeleteTaskRequest(BaseModel):
    task_id: int




