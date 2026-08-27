from typing import Annotated
from fastapi import Depends

from app.core.dependencies import DBSession
from .repository import ProductRepository
from .service import ProductService
from .schemas import ProductQuery


def get_product_repository(session: DBSession) -> ProductRepository:
    return ProductRepository(session)


def get_product_service(
    session: DBSession, repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(session=session, repo=repo)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

ProductQueryDep = Annotated[ProductQuery, Depends()]
