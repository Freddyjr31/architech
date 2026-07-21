# ArchiTech API — Sistema de Gestión de Tareas

API REST desarrollada con **FastAPI** para la gestión de proyectos y tareas con autenticación JWT.

## Stack

- **Framework:** FastAPI
- **Base de datos:** PostgreSQL (vía Supabase) / SQLite (local)
- **ORM:** SQLAlchemy 2.0
- **Autenticación:** JWT con `python-jose` + bcrypt
- **Contenedor:** Docker + docker-compose

## Funcionalidades

- Registro de usuarios
- Autenticación con JWT
- Creación y gestión de proyectos
- Creación y asignación de tareas
- Middleware de logging y trazabilidad por request
- Validación CORS

## Requisitos

- Python 3.12+
- Docker (opcional)

## Instalación y ejecución

```bash
# Clonar el repositorio
git clone git@github.com:Freddyjr31/architech.git
cd architech-system

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Configurar opencode (opcional)
cp opencode.example.json opencode.json
# Editar opencode.json con tu API key de Context7

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload
```

### Con Docker

```bash
docker compose up --build
```

> Las variables de entorno se cargan automáticamente desde `.env` gracias a `env_file: .env` en `docker-compose.yaml`.

La API estará disponible en `http://localhost:8000`.

Documentación interactiva en:
- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Estructura del proyecto

```
├── .opencode/                  # Comandos y skills para opencode
│   ├── commands/
│   │   ├── endpoints.md
│   │   └── serve.md
│   └── skills/
│       └── fastapi/
├── opencode.example.json       # Template de configuración de opencode
├── AGENTS.md                   # Contexto para asistentes IA
├── CHANGELOG.md                # Historial de versiones
├── app/
│   ├── core/                   # Configuración, seguridad, DB, middlewares
│   │   ├── config.py           # Settings + constante VERSION
│   │   ├── database.py         # Engine, session, Base
│   │   ├── dependencies.py     # get_current_user (JWT)
│   │   ├── error_handlers.py   # Manejador centralizado de errores
│   │   ├── logger.py           # Logger estructurado
│   │   ├── middleware.py       # CORS + LogMiddleware
│   │   └── security.py         # JWT + bcrypt
│   ├── models/                 # Modelos SQLAlchemy (ORM)
│   │   ├── __init__.py         # Carga centralizada de modelos
│   │   ├── users_model.py
│   │   ├── projects_model.py
│   │   ├── projects_members_model.py
│   │   ├── projects_roles_model.py
│   │   ├── status_process_model.py
│   │   └── tasks_model.py
│   ├── schemas/                # Schemas compartidos
│   │   └── schemas.py          # TokenPayload, ErrorResponse
│   ├── features/               # Módulos por funcionalidad (Clean Architecture)
│   │   ├── auth/
│   │   │   ├── domain/
│   │   │   │   └── entities.py         # UserEntity
│   │   │   ├── repository/
│   │   │   │   ├── auth_repository_interface.py
│   │   │   │   └── auth_repository_impl.py
│   │   │   ├── services/
│   │   │   │   └── auth_service.py     # AuthService
│   │   │   ├── schemas/
│   │   │   │   └── auth_schemas.py
│   │   │   ├── routes/
│   │   │   │   └── auth_routes.py
│   │   │   ├── dependencies.py         # DI: get_db → get_repository → get_service
│   │   │   └── exceptions.py
│   │   ├── sign_up/
│   │   │   ├── domain/
│   │   │   │   └── entities.py         # UserSignUpEntity
│   │   │   ├── repository/
│   │   │   │   ├── signup_repository_interface.py
│   │   │   │   └── signup_repository_impl.py
│   │   │   ├── services/
│   │   │   │   └── sign_up_service.py  # SignUpService
│   │   │   ├── schemas/
│   │   │   │   └── sign_up_schemas.py
│   │   │   ├── routes/
│   │   │   │   └── sign_up_routes.py
│   │   │   ├── dependencies.py
│   │   │   └── exceptions.py
│   │   ├── projects/
│   │   │   ├── domain/
│   │   │   │   └── entities.py                 # ProjectEntity, ProjectMemberEntity
│   │   │   ├── repository/
│   │   │   │   ├── project_repository_interface.py
│   │   │   │   └── project_repository_impl.py
│   │   │   ├── services/
│   │   │   │   └── project_services.py         # ProjectService
│   │   │   ├── schemas/
│   │   │   │   └── project_schemas.py
│   │   │   ├── routes/
│   │   │   │   └── projects_routes.py
│   │   │   ├── dependencies.py
│   │   │   └── exceptions.py
│   │   └── tasks/
│   │       ├── schemas/
│   │       └── services/
│   ├── routes/                 # Endpoints legacy (comentados, migrados a features/)
│   │   ├── __init__.py         # Importa routers desde features/
│   │   ├── health_routes.py
│   │   └── task_routes.py
│   └── main.py                 # Punto de entrada (FastAPI + lifespan)
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
└── .gitignore
```

## OpenCode (asistente IA)

Este proyecto incluye configuración para [opencode](https://opencode.ai), un asistente de IA para terminal.

### `opencode.json`
Configuración del asistente con integración a Context7 para documentación de librerías.
**Contiene tu API key personal**, por lo que está en `.gitignore`.

```bash
cp opencode.example.json opencode.json
# Editar opencode.json con tu API key de Context7
```

### `.opencode/`
Comandos personalizados y skills para opencode que se cargan automáticamente:

- `commands/serve.md` — Inicia el servidor de desarrollo
- `commands/endpoints.md` — Lista todos los endpoints de la API
- `skills/fastapi/` — Skill oficial de FastAPI con referencias de mejores prácticas

## Variables de entorno

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | URL de conexión a la base de datos |
| `DATABASE_TYPE` | Tipo de BD: `postgresql` o `sqlite` |
| `SECRET_KEY_JWT` | Clave secreta para firmar JWT |
| `ALGORITHIM_HASH_JWT` | Algoritmo de hash (ej. HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de expiración del token |
