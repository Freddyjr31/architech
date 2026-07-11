# AGENTS.md — Contexto para asistentes IA

## Proyecto

ArchiTech API — Sistema de gestión de tareas construido con FastAPI + SQLAlchemy + JWT.

## Stack técnico

- **Python 3.12**
- **FastAPI** — framework web
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL / SQLite** — base de datos
- **python-jose** — JWT
- **passlib[bcrypt]** — hashing de contraseñas
- **pydantic** — validación de schemas
- **Uvicorn** — servidor ASGI
- **Docker** — contenedor

## Convenciones del código

- Los imports siguen el orden: estándar → terceros → locales
- Los archivos terminan con una línea en blanco
- Comentarios con `#?` para secciones, `#*` para notas importantes
- Tipado: se usa type hints de Python (PEP 484)
- ORM: SQLAlchemy 2.0 style (declarative)
- Rutas: prefijo `/api/v1/` con APIRouter
- Schemas Pydantic separados del modelo BD
- Servicios separados de rutas

## Estructura

```
app/
├── core/               # Configuración, seguridad, DB, middlewares
│   ├── config.py       # Settings con pydantic-settings
│   ├── database.py     # Engine, session, Base
│   ├── middleware.py   # CORS + LogMiddleware
│   └── security.py     # JWT + bcrypt
├── features/           # Módulos por funcionalidad
│   ├── auth/           # Autenticación (login)
│   └── sign_up/        # Registro de usuarios
├── routes/             # Endpoints vía APIRouter
│   ├── auth_routes.py
│   └── sign_up_routes.py
└── main.py             # Punto de entrada FastAPI
```

## Comandos útiles

```bash
# Iniciar servidor de desarrollo
uvicorn app.main:app --reload

# Construir y ejecutar con Docker
docker compose up --build

# Instalar dependencias
pip install -r requirements.txt
```

## Reglas al modificar código

1. **No romper** la estructura de carpetas existente
2. **Seguir el patrón** de rutas/schemas/servicios usado en `features/`
3. **No exponer** secretos ni credenciales (`.env` ya está en `.gitignore`)
4. **No agregar archivos** que no sean necesarios (evitar READMEs internos)
5. **Mantener** el tipado y los comentarios existentes
6. **Usar** SQLAlchemy 2.0 style declarative para modelos nuevos
