# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import get_settings

#* Obtiene la instancia de Settings
settings = get_settings()

# Usa DATABASE_URL de tus settings
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # Base para tus modelos SQLAlchemy

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()