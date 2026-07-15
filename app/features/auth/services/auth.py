
from features.auth.exeptions import AuthError, UserNotFoundError
from core.logger import logger
from models.users_model import UserModel

def verify_user(username: str, db):
    """
    - Verifica si un usuario existe en la base de datos.
    """
    try:
        existing_user = db.query(UserModel).filter_by(username=username).first()
        
        #* Si el usuario no existe, retorna None
        if not existing_user:
            logger.warning(f"Usuario '{username}' no encontrado en la base de datos.")
            raise UserNotFoundError(username)
        
        return existing_user
    
    except Exception as e:
        raise AuthError(f"Error al verificar el usuario: {str(e)}")