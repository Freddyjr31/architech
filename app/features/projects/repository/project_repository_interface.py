from abc import ABC, abstractmethod
from features.projects.domain.entities import ProjectEntity

class ProjectRepositoryInterface(ABC):
    
    @abstractmethod
    def project_exists_by_title(self, title: str) -> bool:
        pass
    
    @abstractmethod
    def get_project_by_id(self, id_project: int) -> ProjectEntity | None:
        pass
    
    @abstractmethod
    def create_project(self, project: ProjectEntity, owner_id: int) -> ProjectEntity:
        pass
    
    @abstractmethod
    def is_project_owner(self, project_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def delete_project_with_members(self, id_project: int) -> None:
        pass