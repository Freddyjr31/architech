from pydantic import BaseModel, Field

class UserLoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)

class ChangePasswordRequest(BaseModel):
    # old_password: str = Field(min_length=8, max_length=100)
    new_password: str = Field(min_length=8, max_length=100)
    
class ChangePasswordResponse(BaseModel):
    message: str