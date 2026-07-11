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
git clone <repo-url>
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
├── .opencode/              # Comandos y skills para opencode
│   ├── commands/
│   │   ├── endpoints.md
│   │   └── serve.md
│   └── skills/
│       └── fastapi/
├── opencode.example.json   # Template de configuración de opencode
├── AGENTS.md               # Contexto para asistentes IA
├── app/
│   ├── core/               # Configuración, seguridad, DB, middlewares
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── middleware.py
│   │   └── security.py
│   ├── schemas/
│   ├── models/
│   ├── features/           # Módulos por funcionalidad
│   │   ├── auth/
│   │   └── sign_up/
│   ├── routes/             # Endpoints de la API
│   │   ├── auth_routes.py
│   │   └── sign_up_routes.py
│   └── main.py             # Punto de entrada
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
