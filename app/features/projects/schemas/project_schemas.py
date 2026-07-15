from datetime import datetime
from pydantic import BaseModel, Field

class CreateProjectRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=200)

class CreateProjectResponse(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=200)
    created_at: datetime = Field(..., description="Fecha de creación del usuario")
    message: str = Field(..., description="Mensaje de éxito del registro")
    
class DeleteProjectRequest(BaseModel):
    project_id: int
    

