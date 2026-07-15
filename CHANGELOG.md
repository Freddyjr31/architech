# Changelog

Todas las versiones notables del proyecto ArchiTech API.

Formato basado en [Keep a Changelog](https://keepachangelog.com/) y [SemVer](https://semver.org/).

---

## [1.0.1] — 2026-07-10

Commit inicial de la API.

### Added

- **Estructura base:** FastAPI + SQLAlchemy 2.0 + JWT con `python-jose`
- **Autenticación:** Endpoint `POST /api/v1/auth/login` con JWT y bcrypt
- **Registro:** Endpoint `POST /api/v1/sign-up/create-user` con validación de duplicados
- **Proyectos:** Endpoint `POST /api/v1/proyect/create-project` (esquema `proyects`)
- **Tareas:** Endpoints CRUD básicos (`POST /api/v1/task/create-task`, `DELETE /api/v1/task/delete-task/{id}`, `GET /api/v1/task/get-tasks`)
- **Modelos:** `UserModel`, `ProyectModel`, `ProyectsMembersModel`, `ProyectsRolesModel`, `TasksModel`, `StatusProcessModel`
- **Seguridad:** Hashing de contraseñas con `passlib[bcrypt]`, generación y validación de tokens JWT
- **Infraestructura:** Docker + docker-compose, logger estructurado, CORS, variables de entorno con `pydantic-settings`
- **Schemas Pydantic** separados de los modelos de BD

---

## [1.0.3] — No publicado

Refactorización profunda del manejador de errores y corrección de nomenclatura (`proyects` → `projects`).

### Added

- **Excepciones propias por módulo:**
  - `features/auth/exeptions.py`: `AuthError`, `UserNotFoundError`, `InvalidCredentialsError`
  - `features/sign_up/exeptions.py`: `SignUpError`, `UserNameAlreadyExistsError`, `EmailAlreadyExistsError`
  - `features/projects/exceptions.py`: `ProjectError`, `ProjectNotFoundError`, `ProjectNameTakenError`, `StatusNotFoundError`, `MemberAlreadyAssignedError`, `NotPermissionToDelete`
  - `features/tasks/exeptions.py` (archivo base)

- **Manejador de errores centralizado** en `core/error_handlers.py` — función `register_error_handlers(app)` que registra todos los handlers personalizados:
  - `ProjectNameTakenError` → 409
  - `ProjectNotFoundError` → 404
  - `NotPermissionToDelete` → 403
  - `MemberAlreadyAssignedError` → 400
  - `InvalidCredentialsError` → 401
  - `UserNameAlreadyExistsError`, `EmailAlreadyExistsError` → 409
  - `RequestValidationError` → 422 con detalles de validación
  - Catch-all `Exception` → 500 genérico (sin leaks de trazabilidad)

- **Dependencia de autenticación reutilizable** en `core/dependencies.py`:
  - `get_current_user` como dependencia global vía `HTTPBearer`
  - Type alias `CurrentUser = Annotated[dict, Depends(get_current_user)]`

- **Servicio de eliminación de proyectos** con verificación de permisos (`delete_Project_service`)

### Changed

- **Renombrado módulo `proyects` → `projects`**:
  - Modelos: `ProyectModel` → `ProjectModel`, `ProyectsMembersModel` → `ProjectsMembersModel`, `ProyectsRolesModel` → `ProjectsRolesModel`
  - Archivos movidos de `app/features/proyects/` a `app/features/projects/`
  - Tablas BD renombradas: `proyects` → `projects`, `proyects_members` → `projects_members`
  - Actualizadas todas las referencias en rutas, servicios y __init__

- **Servicios desacoplados de FastAPI**: eliminado `HTTPException` de `features/auth/services/auth.py`, `features/sign_up/services/sign_up_service.py` y `features/projects/services/project_services.py` — ahora usan exclusivamente sus excepciones propias

- **Ruta de proyectos (`project_routes.py`)**:
  - Prefix cambiado de `/api/v1/proyect` a `/api/v1/projects`
  - Agregada dependencia `get_current_user` global vía router
  - Endpoint `create_Project` con manejo de errores y rollback transaccional
  - Endpoint `delete_Project` con verificación de permisos

- **Ruta de autenticación (`auth_routes.py`)**:
  - Login retorna `InvalidCredentialsError` en lugar de `HTTPException` directa
  - Token JWT ahora incluye `user_id` y `username` en el payload

- **Ruta de tareas (`task_routes.py`)**: agregada dependencia `get_current_user` global vía router
- **Modelo `status_process_model.py`**: corregido nombre de clase y tabla (`ProyectsRolesModel` → `StatusModel`, `proyects_roles` → `status_process`)
- **Modelo `tasks_model.py`**: campo `proyect_id` renombrado a `project_id`
- **Versión de la API**: `1.0.2` → `1.0.3` (luego `1.1.0` en este changelog)
- **`main.py`**: handlers de error movidos a `register_error_handlers(app)`, limpieza de imports y formato

### Fixed

- **Typo en README**: URL de clonado corregida (`git@github.com:Freddyjr31/architech.git`)
- **Import de schemas en task_routes.py**: corregido de `app.features.tasks...` a `features.tasks...`
- **Import de `BaseModel` en schemas**: corregido de `fastapi.BaseModel` a `pydantic.BaseModel`
- **Comentarios en security.py**: estandarizados (`#*` → `#?`)

### Removed

- **Archivos antiguos** con nomenclatura `proyects_*`:
  - `app/models/proyects_model.py`
  - `app/models/proyects_members_model.py`
  - `app/models/proyects_roles_model.py`
  - `app/features/proyects/schemas/proyect_schemas.py`
- **Código muerto**: bloque `except HTTPException` inalcanzable en `save_members_to_Project`, variable `dict_proyect` en service

---


