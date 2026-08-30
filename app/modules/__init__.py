from fastapi import FastAPI

from .brands.router import router as router_brand
from .products.router import router as router_products
from .sales.router import router as router_sales
from .restock.router import router as router_restock


def include_router(app: FastAPI) -> None:
    app.include_router(router_brand)
    app.include_router(router_products)
    app.include_router(router_sales)
    app.include_router(router_restock)
