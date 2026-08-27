from fastapi import FastAPI

from app.modules import include_router
from app.core.handlers import register_exception_handler


def create_app():
    app = FastAPI()

    include_router(app)
    register_exception_handler(app)

    return app


app = create_app()
