from features.auth.schemas.auth_schemas import ChangePasswordRequest, UserLoginRequest
from features.auth.repository.auth_repository_interface import AuthRepositoryInterface
from features.auth.exceptions import ErrorChangingPassword, UserNotFoundError, InvalidCredentialsError

from core import security
from core.logger import logger

from schemas.schemas import TokenPayload

class AuthService:
    def __init__(self, auth_repository: AuthRepositoryInterface):
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
        
    def delete_user(self, user_id: int):
        return self.auth_repository.delete_user(user_id)
    
    def change_user_password_service(self, id_user: int, new_password_payload: ChangePasswordRequest):
        #* hasheo la contraseña
        logger.info(f"Intento de cambio de contraseña para el usuario: {id_user} con la nueva contraseña: {new_password_payload.new_password}")
        hashed_password = security.hash_password(new_password_payload.new_password)
        result = self.auth_repository.change_user_password(id_user, hashed_password)
        if not result:
            logger.warning(f"Error al cambiar la contraseña del usuario: {id_user}")
            raise ErrorChangingPassword