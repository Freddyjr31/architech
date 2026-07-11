from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from core.database import Base

class TasksModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title_task = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    proyect_id = Column(Integer, nullable=False)
    status_id = Column(Integer, default=True)
    date_init = Column(TIMESTAMP(timezone=True), nullable=False)
    date_finish = Column(TIMESTAMP(timezone=True), nullable=False)
    owner_id = Column(Integer, nullable=False)
    assigned_id = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)