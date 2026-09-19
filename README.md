# Voltik

API de gestión de stock, ventas y reposición para reemplazar el control manual (lápiz y papel) de inventario de baterías.

## Stack

- **FastAPI** + **SQLAlchemy 2.0 (async)** + **PostgreSQL**
- **Alembic** para migraciones
- **Pydantic v2** para schemas/validación
- **JWT** (PyJWT) + **pwdlib/argon2** para autenticación
- **Pytest** (async) para testing, con SQLite en memoria

## Arquitectura

Cada módulo de negocio (`app/modules/<nombre>`) sigue la misma estructura en capas:

```
router.py        # Endpoints HTTP, sin lógica de negocio
service.py        # Reglas de negocio, orquesta repository(s)
repository.py      # Acceso a datos (SQLAlchemy)
schemas.py        # Pydantic: entrada/salida
models.py         # Modelos ORM
dependencies.py     # Inyección de dependencias (Depends)
```

Módulos: `auth`, `users`, `brands`, `products`, `sales`, `restock`.

Errores de negocio se manejan con excepciones propias (`app/core/exceptions.py`) capturadas por un handler central (`app/core/handlers.py`) que las traduce a respuestas HTTP consistentes.

## Requisitos

- Python 3.12+
- PostgreSQL corriendo localmente (o accesible por red)

## Setup

1. Crear entorno virtual e instalar dependencias:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copiar el archivo de variables de entorno y completarlo:

   ```bash
   cp .env.example .env
   ```

   Generar un `SECRET_KEY` random:

   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

3. Crear la base de datos en Postgres (el nombre debe coincidir con `DATABASE_URL`/`DATABASE_URL_SYNC` en `.env`).

4. Aplicar migraciones:

   ```bash
   alembic upgrade head
   ```

5. Levantar la API:

   ```bash
   uvicorn app.main:app --reload
   ```

   Docs interactivas en `http://localhost:8000/docs`.

## Roles y permisos

- `brands`, `products`, `users`: solo `admin`.
- `sales`, `restock`: cualquier usuario autenticado.
- Login: `POST /auth/login` (OAuth2 password flow) devuelve un JWT.

## Tests

```bash
pytest app/test/ -q
```

Usan una base SQLite en memoria (no tocan la base de Postgres real). Los fixtures compartidos están en `app/test/conftest.py`.

## Migraciones

Crear una nueva migración tras cambiar un modelo:

```bash
alembic revision --autogenerate -m "descripción del cambio"
alembic upgrade head
```
