
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from core.database import Base

class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    id_status = Column(Integer, ForeignKey("status_process.id"), default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    # updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'), nullable=False)
    
    status = relationship("StatusModel")
    members = relationship("ProjectsMembersModel", back_populates="project")
    tasks = relationship("TaskModel", back_populates="project")