from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class ProyectsRolesModel(Base):
    __tablename__ = "proyects_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    can_edit = Column(Boolean, default=False)
    can_assign_task = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)