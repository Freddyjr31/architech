from fastapi import Request, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from core.logger import logger

# ── projects ──
from features.projects.exceptions import (
    ProjectError as ProjectError,
    ProjectNameTakenError,
    ProjectNotFoundError,
    StatusNotFoundError,
    MemberAlreadyAssignedError,
    NotPermissionToDelete
)

# ── Auth ──
from features.auth.exceptions import (
    AuthError as AuthError,
    UserNotFoundError,
    InvalidCredentialsError
)

# ── Sign Up ──
from features.sign_up.exceptions import (
    SignUpError as SignUpError,
    UserNameAlreadyExistsError,
    EmailAlreadyExistsError
    )

def register_error_handlers(app: FastAPI) -> None:
    """Registra todos los exception handlers de la aplicación."""
    
    # ──────────── Auth ────────────

    @app.exception_handler(AuthError)
    def _(request: Request, exc: AuthError):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})
    
    @app.exception_handler(UserNotFoundError)
    def _(request: Request, exc: UserNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsError)
    def _(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})
    
    # ──────────── Sign Up ────────────
    
    @app.exception_handler(SignUpError)
    def _(request: Request, exc: SignUpError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})
    
    @app.exception_handler(UserNameAlreadyExistsError)
    def _(request: Request, exc: UserNameAlreadyExistsError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(EmailAlreadyExistsError)
    def _(request: Request, exc: EmailAlreadyExistsError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    # ──────────── projects ────────────

    @app.exception_handler(ProjectNameTakenError)
    def _(request: Request, exc: ProjectNameTakenError):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(ProjectNotFoundError)
    def _(request: Request, exc: ProjectNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(MemberAlreadyAssignedError)
    def _(request: Request, exc: MemberAlreadyAssignedError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})

    @app.exception_handler(StatusNotFoundError)
    def _(request: Request, exc: StatusNotFoundError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Error de configuración interna."})

    @app.exception_handler(ProjectError)
    def _(request: Request, exc: ProjectError):
        logger.error(f"Error inesperado en projects: {exc}", exc_info=True)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Error interno del servidor."})
    
    @app.exception_handler(NotPermissionToDelete)
    def _(request: Request, exc: NotPermissionToDelete):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "No tienes permiso para eliminar este proyecto."})


    # ──────────── Catch-all global ────────────
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Puedes procesar 'exc.errors()' para limpiar el mensaje
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Datos de entrada inválidos",
                "errors": exc.errors()  # Lista detallada de qué campo falló y por qué
            },
        )

    @app.exception_handler(Exception)
    def _(request: Request, exc: Exception):
        logger.error(f"Excepción no manejada: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"detail": "Error interno del servidor."
        }
    )