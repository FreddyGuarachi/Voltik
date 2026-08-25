from fastapi import FastAPI

from app.modules.brands.router import router
from app.core.handlers import register_exception_handler


def create_app():
    app = FastAPI()

    app.include_router(router)
    register_exception_handler(app)

    return app


app = create_app()
