from features.sign_up.domain.entities import UserSignUpEntity
from features.sign_up.repository.signup_repository_interface import SignUpRepositoryInterface
from features.sign_up.exceptions import EmailAlreadyExistsError, UserNameAlreadyExistsError
from features.sign_up.schemas.sign_up_schemas import UserRegisterRequest

from core.logger import logger
from core.security import hash_password

class SignUpService:
    def __init__(self, repository: SignUpRepositoryInterface):
        self.repository = repository
        
    def register_user(self, user_data: UserRegisterRequest):
        """
        - Valida una existencia previa del usuario y correo para notificar si ya esta creado
        - Registra un nuevo usuario en la base de datos.
        """
        
        logger.info(f"Intento de registro para usuario: {user_data.username}")
        
        #* verifico si el usuario ya existe en la base de datos
        existing_user = self.repository.get_user_by_username(user_data.username)
        if existing_user:
            logger.warning(f"Registro fallido: el username '{user_data.username}' ya existe.")
            raise UserNameAlreadyExistsError(user_data.username)
        
        #* verifico si el correo electrónico ya existe en la base de datos
        existing_email = self.repository.get_user_by_email(user_data.email)
        if existing_email:
            logger.warning(f"Registro fallido: el correo electrónico '{user_data.email}' ya está en uso.")
            raise EmailAlreadyExistsError(user_data.email)
        
        #* Lógica para registrar al usuario
        new_user = UserSignUpEntity(
            id=None,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        
        #* Guardar el nuevo usuario en la base de datos
        return self.repository.register_user(new_user)