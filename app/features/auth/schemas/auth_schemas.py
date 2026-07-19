from pydantic import BaseModel, Field

class UserLoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    
# class UserLoginResponse(BaseModel):
#     access_token: str = Field(..., description="Token de acceso")
#     token_type: str = Field(..., description="Tipo de token")

class TokenPayload(BaseModel):
    username: str
    user_id: int