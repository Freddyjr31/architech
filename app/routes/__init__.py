"""
Inicializador del paquete de rutas.

Centraliza el registro de todos los routers de la aplicación.
Para añadir un nuevo módulo:
  1. Crea el router en features/modulo/routes
  2. Impórtalo en routes/__init__.py
"""

from fastapi import FastAPI

# from .auth_routes import router as auth_router
# from .sign_up_routes import router as sign_up_router
# from .project_routes import router as project_router
from .task_routes import router as task_router
from .health_routes import router as health_router

#? ---- Nuevos imports
from features.auth.routes.auth_routes import router as auth_router
from features.sign_up.routes.sign_up_routes import router as sign_up_router
from features.projects.routes.projects_routes import router as project_router

def register_all_routers(app: FastAPI) -> None:
    """
    Registra todos los routers de la aplicación en la instancia de FastAPI.

    Organización:
      - Rutas base:   auth | sign_up | project | task
    """
    
    app.include_router(auth_router)
    app.include_router(sign_up_router)
    app.include_router(project_router)
    app.include_router(task_router)
    app.include_router(health_router)
