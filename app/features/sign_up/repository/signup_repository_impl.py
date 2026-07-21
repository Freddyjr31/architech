
from features.sign_up.repository.signup_repository_interface import SignUpRepositoryInterface
from features.sign_up.domain.entities import UserSignUpEntity
from models.users_model import UserModel
from sqlalchemy.orm import Session

class SignUpRepositoryImpl(SignUpRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db
        
    def get_user_by_username(self, username: str):
        return self.db.query(UserModel).filter_by(username=username).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter_by(email=email).first()
        
    def register_user(self, user_entity: UserSignUpEntity):
        try:
            #* mappear el UserSignUpEntity a UserModel
            user_to_create = UserModel(
                username=user_entity.username,
                email=user_entity.email,
                hashed_password=user_entity.hashed_password
            )
            
            self.db.add(user_to_create)
            self.db.commit()
            self.db.refresh(user_to_create)
            
            return UserSignUpEntity(
                id=user_to_create.id,
                username=user_to_create.username,
                email=user_to_create.email,
                hashed_password=user_to_create.hashed_password,
                created_at=user_to_create.created_at,
                updated_at=user_to_create.updated_at
            )
            
        except Exception as e:
            self.db.rollback()
            raise