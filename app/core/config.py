from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

#? ----- Project version
VERSION = "1.0.9"

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)
    
    #? ──────────────────────────────────────────────
    #?        Configuración de base de datos
    #? ──────────────────────────────────────────────

    # URL de conexión a la base de datos principal
    DATABASE_URL: str = "sqlite:///./app.db"

    # Tipo de base de datos: "postgresql" | "sqlite" | "mysql"
    DATABASE_TYPE: str = "postgresql"

    # Activar logs detallados de SQLAlchemy (útil en desarrollo)
    DATABASE_ECHO: bool = True

    #? ──────────────────────────────────────────────
    #?               JWT (Autenticación)
    #? ──────────────────────────────────────────────

    SECRET_KEY_JWT: str
    ALGORITHIM_HASH_JWT: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


# @lru_cache asegura que la instancia de Settings se cree una sola vez
# y se reutilice en toda la aplicación, mejorando el rendimiento.
@lru_cache()
def get_settings():
    return Settings()
