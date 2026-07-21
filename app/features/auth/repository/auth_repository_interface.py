
from abc import ABC, abstractmethod
from features.auth.domain.entities import UserEntity

class AuthRepositoryInterface(ABC):
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> UserEntity | None:
        pass