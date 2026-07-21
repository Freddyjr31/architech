
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from features.projects.exceptions import StatusNotFoundError
from models.projects_members_model import ProjectsMembersModel
from features.projects.domain.entities import ProjectEntity
from features.projects.repository.project_repository_interface import ProjectRepositoryInterface

from models.projects_model import ProjectModel
from models.status_process_model import StatusModel

class ProjectRepositoryImpl(ProjectRepositoryInterface):
    
    def __init__(self, db: Session):
        self.db = db
        
    def _resolve_status_id(self, status_name) -> int:
        status = self.db.query(StatusModel).filter_by(name=status_name, type="project").first()
        if status is None:
            raise StatusNotFoundError(status_name)
        return status.id
    
    def _model_to_entity(self, model: ProjectModel) -> ProjectEntity:
        return ProjectEntity(
            id=model.id,
            title=model.title,
            description=model.description,
            status_name=model.status.name if model.status else None,
            created_at=model.created_at
        )
    
        
    def project_exists_by_title(self, title: str) -> bool:
        existing_project = self.db.query(ProjectModel).filter_by(title=title).first()
        return existing_project is not None
    
    def get_project_by_id(self, id_project: int) -> ProjectEntity | None:
        project = self.db.query(ProjectModel).filter_by(id=id_project).first()
        if not project: return None
        return self._model_to_entity(project)
    
    def create_project(self, project: ProjectEntity, owner_id: int) -> ProjectEntity:
        try:
            
            new_project = ProjectModel(
                title=project.title,
                description=project.description,
                id_status=self._resolve_status_id(project.status_name),
                # created_at=datetime.now(timezone.utc),
            )
            
            self.db.add(new_project)
            self.db.flush()
            
            #? Agregar miembros
            member = ProjectsMembersModel(
                project_id=new_project.id,
                user_id=owner_id,
                role_id=self._resolve_status_id(project.status_name),
            )
            
            self.db.add(member)
            self.db.commit()
            self.db.refresh(new_project)
            
            return  self._model_to_entity(new_project)
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def is_project_owner(self, project_id: int, user_id: int) -> bool:
        return self.db.query(ProjectsMembersModel).filter_by(
            project_id=project_id,
            user_id=user_id,
            role_id=1).first() is not None
        
    
    def delete_project_with_members(self, id_project) -> None:
        
        self.db.query(ProjectsMembersModel).filter_by(
            project_id=id_project
        ).delete(synchronize_session=False)

        project = self.db.query(ProjectModel).filter_by(id=id_project).first()
        if project:
            self.db.delete(project)

        self.db.commit()