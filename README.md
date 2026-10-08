# Voltik

A small app to keep track of battery stock at work: products, brands, sales and restocks.
The idea is to stop doing it with pen and paper.

- **Backend:** FastAPI + SQLAlchemy (async) + PostgreSQL, with Alembic for migrations.
- **Frontend:** plain HTML/CSS/JS in `frontend/`, no frameworks.

## Getting started

You need Python 3.12+ and PostgreSQL running.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with your database info. For `SECRET_KEY`, generate a random one:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Create the database in Postgres (same name as in `.env`), then run the migrations:

```bash
alembic upgrade head
```

## Creating the first admin

Only an admin can create users, so the first one has to be added by hand.
From the project root (change the name and password):

```bash
python -c "
import asyncio
from app.db.session import SessionLocal
from app.modules.users.models import User, UserRole
from app.core.security import get_password_hash

async def main():
    async with SessionLocal() as session:
        session.add(User(user_name='admin', password_hash=get_password_hash('admin1234'), role=UserRole.ADMIN))
        await session.commit()

asyncio.run(main())
"
```

## Running it

Start the API:

```bash
uvicorn app.main:app --reload
```

It runs on `http://127.0.0.1:8000`, and the docs are at `/docs`.

For the frontend, open `frontend/index.html` with VS Code's Live Server. It runs on
`http://127.0.0.1:5500`.

If you open the frontend from a different address, add it to `CORS_ORIGINS` in `.env`,
otherwise the browser blocks the requests:

```
CORS_ORIGINS=["http://127.0.0.1:5500"]
```

## Who can do what

There are two roles: `admin` and `seller`.

- **Everyone logged in:** see products, register sales and restocks, export the stock.
- **Admin only:** create, edit and delete products and brands, and manage users.

Deleting a product or brand that already has movements doesn't really delete it.
It just gets marked as inactive, so the history stays intact.

## Stock export

`GET /product/export?format=csv` downloads a CSV with every active product and its stock,
plus two empty columns ("Conteo real" and "Diferencia") to fill in when you count the
real stock. The "Descargar stock" button in the frontend does the same thing.

## Project layout

Each module in `app/modules/` (`auth`, `users`, `brands`, `products`, `sales`, `restock`)
has the same files:

- `router.py`: the endpoints
- `service.py`: the business rules
- `repository.py`: the database queries
- `schemas.py`: Pydantic models for input/output
- `models.py`: SQLAlchemy models
- `dependencies.py`: wires everything together with `Depends`

Custom errors live in `app/core/exceptions.py`. They are turned into HTTP responses in
`app/core/handlers.py`.

## Tests

```bash
pytest app/test/ -q
```

They use an in-memory SQLite database, so your real data is never touched.

## Migrations

After changing a model:

```bash
alembic revision --autogenerate -m "what changed"
alembic upgrade head
```
