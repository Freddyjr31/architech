from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from core.database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title_task = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status_process.id"), default=True)
    date_init = Column(TIMESTAMP(timezone=True), nullable=False)
    date_finish = Column(TIMESTAMP(timezone=True), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    project = relationship("ProjectModel", back_populates="tasks")
    owner_tasks = relationship("UserModel", back_populates="owner_tasks", foreign_keys=[owner_id])
    assigned = relationship("UserModel", back_populates="assigned_tasks", foreign_keys=[assigned_id])
    status = relationship("StatusModel")