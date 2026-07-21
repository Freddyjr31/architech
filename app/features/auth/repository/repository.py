from sqlalchemy.orm import Session
from models.users_model import UserModel

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_user_by_username(self, username: str):
        return self.db.query(UserModel).filter_by(username=username).first()