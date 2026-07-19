from features.auth.schemas.auth_schemas import TokenPayload, UserLoginRequest
from features.auth.repository.repository import AuthRepository
from features.auth.exceptions import UserNotFoundError, InvalidCredentialsError

from core import security
from core.logger import logger

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository
        
    def authenticate_user(self, userPayload: UserLoginRequest):
        
        username = userPayload.username
        password = userPayload.password
        
        user = self.auth_repository.get_user_by_username(username)
        
        #* Si el usuario no existe, retorna None
        if not user:
            logger.warning(f"Usuario '{username}' no encontrado en la base de datos.")
            raise UserNotFoundError(username)
        
        if not security.verify_password(password, user.hashed_password):
            logger.warning(f"Error de autenticación para el usuario: {username}")
            raise InvalidCredentialsError
            
        return TokenPayload(
            username=user.username,
            user_id=user.id
        )