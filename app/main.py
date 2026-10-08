from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules import include_router
from app.core.handlers import register_exception_handler
from app.core.config import setting


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=setting.CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(app)
    register_exception_handler(app)

    return app


app = create_app()
