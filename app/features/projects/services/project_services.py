"""
    Defino los servicios relacionados con los Projectos, incluyendo la creación, eliminación y obtención de Projectos.
"""

from features.projects.schemas.project_schemas import CreateProjectRequest
from features.projects.domain.entities import ProjectEntity
from features.projects.repository.project_repository_interface import ProjectRepositoryInterface
from core.logger import logger
from features.projects.exceptions import (
    NotPermissionToDelete,
    ProjectNameTakenError,
    ProjectNotFoundError
)


class ProjectService:
    """
    Servicios relacionados con los Projectos
    """
    
    def __init__(self, repository: ProjectRepositoryInterface):
        self.repository = repository
        
    def create_project_service(
        self, 
        project_payload: CreateProjectRequest,
        owner_id: int
        ) -> ProjectEntity:
        
        #? primero valido que no exista un Projecto con el mismo nombre
        if self.repository.project_exists_by_title(project_payload.title):
            raise ProjectNameTakenError(project_payload.title)
        
        #* Guardar el nuevo Projecto en la base de datos
        project = ProjectEntity(
            title=project_payload.title,
            description=project_payload.description,
            status_name="En curso",
        )
        
        new_project = self.repository.create_project(project, owner_id)
        
        logger.info(f"Projecto creado exitosamente: {new_project.id} - {new_project.title}")
        
        return new_project
        
    
    def delete_project_service(self, id_project: int, current_user_id: int) -> None:
        """
        Servicio para eliminar un Projecto
        """
        
        #* valido que el Projecto existe
        if not self.repository.get_project_by_id(id_project):
            raise ProjectNotFoundError
        
        #* validar que solo el propietario pueda eliminar el Projecto
        is_owner = self.repository.is_project_owner(id_project, current_user_id)
        if not is_owner:
            raise NotPermissionToDelete
        
        #* elimino el Projecto de la base de datos tabla projects
        self.repository.delete_project_with_members(id_project)

        logger.info(f"Projecto eliminado con éxito: {id_project}")