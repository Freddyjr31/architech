from fastapi import BaseModel, Field
from datetime import datetime

class CreateProyectRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)

class CreateProyectResponse(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    created_at: datetime = Field(..., description="Fecha de creación del usuario")
    message: str = Field(..., description="Mensaje de éxito del registro")
    
class DeleteProyectRequest(BaseModel):
    proyect_id: int




