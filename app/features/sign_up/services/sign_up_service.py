
from fastapi import HTTPException
from core.logger import logger
from features.sign_up.schemas.sign_up_schemas import UserRegisterRequest
from models.users_model import UserModel
from core.security import create_access_token, hash_password

def register_user(user_data: UserRegisterRequest, db):
    """
    - Valida una existencia previa del usuario y correo para notificar si ya esta creado
    - Registra un nuevo usuario en la base de datos.
    """
    
    logger.info(f"Intento de registro para usuario: {user_data.username}")
    
    try:
        #* verifico si el usuario ya existe en la base de datos
        existing_user = db.query(UserModel).filter_by(username=user_data.username).first()
        if existing_user:
            logger.warning(f"Registro fallido: el username '{user_data.username}' ya existe.")
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")
        
        #* verifico si el correo electrónico ya existe en la base de datos
        existing_email = db.query(UserModel).filter_by(email=user_data.email).first()
        if existing_email:
            logger.warning(f"Registro fallido: el correo electrónico '{user_data.email}' ya está en uso.")
            raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso.")
        
        #* Lógica para registrar al usuario (aún no implementada)
        new_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        
        #* Guardar el nuevo usuario en la base de datos
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"Usuario registrado exitosamente: {new_user.id} - {new_user.username}")
        return new_user
    
    except Exception as e:
        db.rollback()
        raise e
    