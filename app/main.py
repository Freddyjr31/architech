
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import register_all_routers
from core.logger import logger

from core.middleware import LogMiddleware, origins

#* Instancia de FastAPI
app = FastAPI(
    title="ArchiTech API",
    version="1.0.2",
    description="API para la gestión de usuarios, proyectos y tareas de ArchiTech",
)

@app.on_event("startup")
def on_startup():
    """
    Evento ejecutado al iniciar la aplicación.
    Inicializa la base de datos y registra el arranque.
    """
    logger.info("Iniciando aplicación FastAPI Auth...")

    logger.info("Aplicación lista para recibir peticiones.")

#? -- Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogMiddleware)

#? -- Rutas de la aplicación
register_all_routers(app)

@app.get("/")
def read_root():
    return {"message": "ArchiTech API its running"}


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
    