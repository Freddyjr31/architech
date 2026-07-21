from abc import ABC, abstractmethod

from features.sign_up.domain.entities import UserSignUpEntity

class SignUpRepositoryInterface(ABC):
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> UserSignUpEntity | None:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> UserSignUpEntity | None:
        pass
    
    @abstractmethod
    def register_user(self, user: UserSignUpEntity) -> UserSignUpEntity:
        pass