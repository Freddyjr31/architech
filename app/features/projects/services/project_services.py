"""
    Defino los servicios relacionados con los Projectos, incluyendo la creación, eliminación y obtención de Projectos.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from core.logger import logger
from features.projects.exceptions import (
    NotPermissionToDelete,
    ProjectNameTakenError,
    StatusNotFoundError,
    ProjectNotFoundError
)
from features.projects.schemas.project_schemas import CreateProjectRequest
from models.projects_members_model import ProjectsMembersModel
from models.projects_model import ProjectModel
from models.status_process_model import StatusModel


def get_in_course_status_id(db: Session) -> int:
    """
    Servicio para obtener el ID del estado "In Course" de la tabla de estados.
    """

    in_course_status = db.query(StatusModel).filter_by(name="En curso", type="project").first()

    if not in_course_status:
        logger.error("Estado 'En Curso' no encontrado en la base de datos.")
        raise StatusNotFoundError()

    return in_course_status.id


def create_project_service(payload: CreateProjectRequest, owner_id: int, db: Session) -> ProjectModel:
    """
    Servicio para crear un Projecto
    """

    #? primero valido que no exista un Projecto con el mismo nombre
    existing_Project = db.query(ProjectModel).filter_by(title=payload.title).first()
    if existing_Project:
        raise ProjectNameTakenError(payload.title)

    #* Guardar el nuevo Projecto en la base de datos
    project = ProjectModel(
        title=payload.title,
        description=payload.description,
        id_status=get_in_course_status_id(db),
        created_at=datetime.now(timezone.utc),
    )

    db.add(project)
    db.flush()
    
     # Agregar miembros (sin commit)
    member = ProjectsMembersModel(
        project_id=project.id,
        user_id=owner_id,
        role_id=1,
        created_at=datetime.now(timezone.utc),
    )
    db.add(member)

    db.commit()
    db.refresh(project)

    logger.info(f"Projecto creado con éxito: {project}")

    return project


# def save_members_to_project(project_id: int, members: list, db: Session) -> None:
#     """
#     Servicio para guardar los miembros de un Projecto
#     """

#     for member in members:
#         existing_member = db.query(ProjectsMembersModel).filter_by(
#             project_id=project_id,
#             user_id=member,
#             role_id=1
#         ).first()

#         if existing_member:
#             raise MemberAlreadyAssignedError(member)

#         new_member = ProjectsMembersModel(
#             project_id=project_id,
#             user_id=member,
#             role_id=1,
#             created_at=datetime.now(timezone.utc),
#         )

#         db.add(new_member)

#     db.commit()


def delete_project_service(project_id: int, current_user_id: int, db: Session) -> None:
    """
    Servicio para eliminar un Projecto
    """
    
    #* valido que el Projecto existe
    project = db.query(ProjectModel).filter_by(id=project_id).first()
    if not project:
        raise ProjectNotFoundError
    
    #* validar que solo el propietario pueda eliminar el Projecto
    is_owner = db.query(ProjectsMembersModel).filter_by(
        project_id=project_id,
        user_id=current_user_id,
        role_id=1
    ).first()
    
    if not is_owner:
        raise NotPermissionToDelete
    
    #* elimino los members de la tabla de Projectos
    db.query(ProjectsMembersModel).filter_by(project_id=project_id).delete(synchronize_session=False)
    
    #* elimino el Projecto de la base de datos tabla projects
    db.delete(project)
    
    db.commit()

    logger.info(f"Projecto eliminado con éxito: {project_id}")
