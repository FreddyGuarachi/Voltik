from fastapi import FastAPI

from .brands.router import router as router_brand
from .products.router import router as router_products


def include_router(app: FastAPI) -> None:
    app.include_router(router_brand)
    app.include_router(router_products)
