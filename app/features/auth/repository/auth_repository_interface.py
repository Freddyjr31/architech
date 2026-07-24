
from abc import ABC, abstractmethod
from features.auth.domain.entities import UserEntity

class AuthRepositoryInterface(ABC):
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> UserEntity | None:
        pass
    
    @abstractmethod
    def delete_user(self, username: str) -> None:
        pass

    @abstractmethod
    def change_user_password(self, user_id: int, new_password: str) -> bool:
        pass