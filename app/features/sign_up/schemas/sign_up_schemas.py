from pydantic import BaseModel, Field
from datetime import datetime

class UserRegisterRequest(BaseModel):
    username:str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8, max_length=100)
    # created_at: datetime
    
class UserRegisterResponse(BaseModel):
    id: int
    username:str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    created_at: datetime = Field(..., description="Fecha de creación del usuario")
    message: str = Field(..., description="Mensaje de éxito del registro")