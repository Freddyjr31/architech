
from sqlalchemy.orm import Session
from models.users_model import UserModel
from features.auth.domain.entities import UserEntity
from features.auth.repository.auth_repository_interface import AuthRepositoryInterface

class AuthRepositoryImpl(AuthRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db
        
    def get_user_by_username(self, username: str) -> UserEntity | None:
        user_in_db = self.db.query(UserModel).filter_by(username=username).first()
        if not user_in_db: return None
        return UserEntity(
            id=user_in_db.id,
            email=user_in_db.email,
            username=user_in_db.username,
            hashed_password=user_in_db.hashed_password,
            created_at=user_in_db.created_at,
            updated_at=user_in_db.updated_at,
        )
        
    def delete_user(self, username: str) -> None:
        
        #* Si el usuario tiene tareas y proyectos asociados, no se puede eliminar
        
        user_in_db = self.db.query(UserModel).filter_by(username=username).first()
        if not user_in_db: return None
        self.db.delete(user_in_db)
        self.db.commit()