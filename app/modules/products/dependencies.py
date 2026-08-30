from typing import Annotated
from fastapi import Depends

from app.core.dependencies import DBSession
from .repository import ProductRepository
from .service import ProductService
from .schemas import ProductQuery
from ..brands.dependencies import BrandServiceDep


def get_product_repository(session: DBSession) -> ProductRepository:
    return ProductRepository(session)


def get_product_service(
    session: DBSession,
    brand_service: BrandServiceDep,
    repo: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    return ProductService(session=session, brand_service=brand_service, repo=repo)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

ProductQueryDep = Annotated[ProductQuery, Depends()]
