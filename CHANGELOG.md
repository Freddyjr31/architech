# Changelog

Todas las versiones notables del proyecto ArchiTech API.

Formato basado en [Keep a Changelog](https://keepachangelog.com/) y [SemVer](https://semver.org/).

---

## [1.0.8] — 2026-07-21

Corrección de bugs finales en el módulo projects tras la migración a Clean Architecture.

### Fixed

- **`project_repository_impl.py`**: corregido `role_id` en `create_project` — usaba `_resolve_status_id(project.status_name)` (resolvía status, no rol). Corregido a `role_id=1` (owner)
- **`project_repository_impl.py`**: eliminado import muerto `datetime, timezone` (ya no se usa en el repository)
- **`project_services.py`**: eliminado `created_at=datetime.now(timezone.utc)` en creación de `ProjectEntity` — la BD resuelve la fecha con `server_default=text('now()')`

### Removed

- **`project_services.py`**: eliminado código comentado de funciones standalone (`get_in_course_status_id`, `create_project_service`, `delete_project_service`) — reemplazado por `ProjectService` class

---

## [1.0.7] — 2026-07-21

Migración del módulo projects a Clean Architecture: domain entities, repository pattern con ABC, inyección de dependencias y corrección de bugs.

### Added

- **`domain/entities.py`** en projects — entidades `ProjectEntity` y `ProjectMemberEntity` como dataclasses puras
- **Capa `repository/`** en projects:
  - `ProjectRepositoryInterface` — contrato abstracto (ABC) con 5 operaciones: `project_exists_by_title`, `get_project_by_id`, `create_project`, `is_project_owner`, `delete_project_with_members`
  - `ProjectRepositoryImpl` — implementación con SQLAlchemy, mapeo ORM ↔ Entity, resolución de status por nombre (`_resolve_status_id`)
- **`dependencies.py`** en projects — cadena de inyección `get_db` → `get_project_repository` → `get_project_service`
- **`ProjectService`** como clase con inyección de repository — `create_project_service` y `delete_project_service` como methods

### Fixed

- **`project_repository_impl.py`**: corregido `is_project_owner` — query cambiada de `ProjectModel` a `ProjectsMembersModel` con filtro `project_id` en vez de `id`
- **`project_repository_impl.py`**: eliminado `created_at` hardcodeado en `create_project` — la BD resuelve con `server_default=text('now()')`
- **`project_services.py`**: service ahora recibe `CreateProjectRequest` en vez de `ProjectEntity` — crea el entity internamente con `status_name="En curso"`
- **`domain/entities.py`**: corregido orden de campos en dataclass — campos sin default (`title`, `description`, `status_name`) antes de campos con default (`id`, `created_at`)

### Changed

- **`project_services.py`**: eliminados imports muertos (`datetime`, `Session`, `StatusNotFoundError`), eliminado código comentado de funciones standalone
- **`projects_routes.py`**: llamadas actualizadas a `service.create_project_service()` y `service.delete_project_service()` (clase inyectada en vez de funciones standalone)

---

## [1.0.6] — 2026-07-20

Migración a Clean Architecture: separación de capas (domain, repository, service) en los módulos auth y sign_up, inyección de dependencias, eliminación de código muerto.

### Added

- **Constante global `VERSION`** en `core/config.py` — única fuente de verdad para la versión del proyecto, utilizada en `FastAPI(version=...)`
- **Capa `domain/entities.py`** en auth y sign_up — entidades `UserEntity` y `UserSignUpEntity` como dataclasses puras, separadas del modelo ORM
- **Capa `repository/`** en auth y sign_up:
  - `AuthRepositoryInterface` y `SignUpRepositoryInterface` — contratos abstractos (ABC) que definen las operaciones de persistencia
  - `AuthRepositoryImpl` y `SignUpRepositoryImpl` — implementaciones concretas con SQLAlchemy que mapean entre entidades de dominio y modelos ORM
- **`dependencies.py`** en auth y sign_up — cadena de inyección de dependencias (`get_db` → `get_*_repository` → `get_*_service`) usando `Annotated[..., Depends()]`
- **`TokenPayload` como Pydantic model** en `auth/schemas/auth_schemas.py` — reemplaza el dict sin tipo para el payload del JWT

### Changed

- **Auth route movido** de `app/routes/auth_routes.py` a `features/auth/routes/auth_routes.py` — el router ahora vive dentro del módulo
- **Sign up route movido** de `app/routes/sign_up_routes.py` a `features/sign_up/routes/sign_up_routes.py`
- **`routes/__init__.py`** actualizado para importar routers desde `features/` en lugar de `app/routes/`
- **Auth service (`AuthService`)**: lógica de autenticación unificada en `authenticate_user()`, recibe repository por inyección en vez de `db` directo
- **Sign up service (`SignUpService`)**: refactorizado a clase con inyección de repository, elimina dependencia directa de `db` y try/except con `self.db.rollback()` inexistente
- **Schemas**: eliminado `Field(...)` con ellipsis en todos los modelos Pydantic (`auth_schemas.py`, `sign_up_schemas.py`)
- **Rutas auth y sign_up**: cambiadas de `async def` a `def` (operaciones sync con SQLAlchemy)

### Fixed

- **`signup_repository_impl.py`**: corregida query a `UserModel` en vez de `UserSignUpEntity` (fallaba en runtime)
- **`signup_repository_impl.py`**: mapeo explícito de `UserSignUpEntity` a `UserModel` al persistir, y viceversa al leer
- **`auth_service.py`**: corregido `verify_password(username, ...)` → `verify_password(password, ...)` (bug de seguridad)

### Removed

- **Código muerto en auth**: `services/auth.py` (función `verify_user`), `repository/repository.py` (clase `AuthRepository` sin ABC)
- **Routers viejos**: `app/routes/auth_routes.py` y `app/routes/sign_up_routes.py` comentados (código migrado a features/)
- **Bloque comentado** en `sign_up_service.py` (función `register_user` antigua, 47 líneas)
- **Error handler duplicado** `@app.exception_handler(Exception)` en `main.py` (ya existía en `error_handlers.py`)

---

## [1.0.4] — 2026-07-16

Corrección de nombre de columna y limpieza de configuración Docker.

### Fixed

- **`tasks_model.py`**: corregido nombre de columna `assigned_id` → `assignne_id` (typo en BD)

### Removed

- **`docker-compose.yaml`**: eliminada clave `version: '3.8'` deprecated en Docker Compose V2

---

## [1.0.3] — 2026-07-16

Refactorización profunda del manejador de errores, atomicidad en transacciones y relationships en modelos.

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

- **Servicio de eliminación de proyectos** con verificación de permisos (`delete_project_service`)

- **`models/__init__.py`** — carga centralizada de todos los modelos SQLAlchemy para garantizar que el registry los conozca al iniciar

- **Relationships en modelos:**
  - `ProjectModel`: `members`, `tasks`
  - `ProjectsMembersModel`: `project`, `user`, `role`
  - `UserModel`: `project_memberships`, `owned_tasks`, `assigned_tasks`

- **`lifespan` context manager** en `main.py` reemplaza `@app.on_event("startup")` deprecated

### Changed

- **Renombrado módulo `proyects` → `projects`**:
  - Modelos: `ProyectModel` → `ProjectModel`, `ProyectsMembersModel` → `ProjectsMembersModel`, `ProyectsRolesModel` → `ProjectsRolesModel`
  - Archivos movidos de `app/features/proyects/` a `app/features/projects/`
  - Tablas BD renombradas: `proyects` → `projects`, `proyects_members` → `projects_members`
  - Actualizadas todas las referencias en rutas, servicios y __init__

- **Servicios desacoplados de FastAPI**: eliminado `HTTPException` de `features/auth/services/auth.py`, `features/sign_up/services/sign_up_service.py` y `features/projects/services/project_services.py` — ahora usan exclusivamente sus excepciones propias

- **Atomicidad en `create_project_service`**: combinado `create_project` + `save_members_to_project` en una sola función con `db.flush()` + un solo `db.commit()` — si falla, todo se revierte

- **`project_services.py`**: eliminado import `MemberAlreadyAssignedError` (no usado), `delete_project_service` type hint `-> bool` → `-> None`, eliminado `return True`

- **`project_routes.py`**: eliminado import y llamada comentada de `save_members_to_project`, simplificado `delete_Project` (eliminado `if` redundante)

- **`sign_up_routes.py`**: agregado try/except con `SignUpError` + `Exception` (patrón consistente con project_routes), eliminado `if new_user:` redundante

- **`sign_up_service.py`**: eliminado import comentado, agregado return type hint `-> UserModel`

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
- **`main.py`**: handlers de error movidos a `register_error_handlers(app)`, agregado `import models` para carga de modelos, `lifespan` context manager

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
- **Código muerto**: bloque `except HTTPException` inalcanzable en `save_members_to_Project`, variable `dict_proyect` en service, imports comentados

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
