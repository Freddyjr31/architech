
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import VERSION
from core.error_handlers import register_error_handlers
from core.logger import logger
from core.middleware import LogMiddleware, origins

from contextlib import asynccontextmanager

from routes import register_all_routers

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
    version=VERSION,
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