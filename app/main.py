
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import models  # noqa: F401 — fuerza carga de todos los modelos SQLAlchemy
from core.error_handlers import register_error_handlers
from routes import register_all_routers
from core.logger import logger
from core.middleware import LogMiddleware, origins
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # inicio de la app
    logger.info("Iniciando la app")
    yield
    # fin de la app
    logger.info("Finalizando la app")

#* Instancia de FastAPI
app = FastAPI(
    title="ArchiTech API",
    version="1.0.4",
    description="API para la gestión de usuarios, proyectos y tareas de ArchiTech",
    lifespan=lifespan
)

#? -- Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogMiddleware)

#? --- Registro las rutas de la aplicación ---
register_all_routers(app)

#? -- Registrar los manejadores de errores personalizados
register_error_handlers(app)

@app.get("/")
def read_root():
    return "ArchiTech API its running"

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    """
    Captura cualquier excepción no manejada y retorna un error 500.
    """
    logger.error(f"Excepción no manejada: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor."},
    )
    