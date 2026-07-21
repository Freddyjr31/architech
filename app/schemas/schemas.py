
from pydantic import BaseModel, Field

# ──────────────────────────────────────────────
# Esquemas para errores genéricos
# ──────────────────────────────────────────────
class ErrorResponse(BaseModel):
    """
    Esquema Pydantic para respuestas de error estandarizadas.
    """
    detail: str

# ──────────────────────────────────────────────
# Esquema para la respuesta con el token JWT
# ──────────────────────────────────────────────
class TokenResponse(BaseModel):
    """
    Esquema Pydantic para la respuesta con el token JWT.
    """
    access_token: str = Field(..., description="Token de acceso")
    token_type: str = "bearer"
    
# ─────────────────────────────────────────────
# Esquema para el payload del token JWT
# ───────────────────────────────────────────── 
class TokenPayload(BaseModel):
    username: str
    user_id: int