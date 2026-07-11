from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from core.database import Base

class ProyectsMembersModel(Base):
    __tablename__ = "proyects_members"

    id = Column(Integer, primary_key=True, index=True)
    proyect_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)