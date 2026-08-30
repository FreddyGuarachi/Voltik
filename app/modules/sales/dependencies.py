from typing import Annotated
from fastapi import Depends

from app.core.dependencies import DBSession
from .repository import SaleRepository
from .service import SaleService
from ..products.dependencies import ProductServiceDep


def get_sale_repository(session: DBSession) -> SaleRepository:
    return SaleRepository(session)


def get_sale_service(
    session: DBSession,
    product_service: ProductServiceDep,
    repo: SaleRepository = Depends(get_sale_repository),
) -> SaleService:
    return SaleService(session=session, repo=repo, product_service=product_service)


SaleServiceDep = Annotated[SaleService, Depends(get_sale_service)]
