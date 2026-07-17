from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from core.database import Base

class ProjectsMembersModel(Base):
    __tablename__ = "projects_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"),  nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("projects_roles.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    project = relationship("ProjectModel", back_populates="members")
    user = relationship("UserModel", back_populates="project_memberships")
    role = relationship("ProjectsRolesModel")
    