from typing import Annotated
from fastapi import Depends

from app.core.dependencies import DBSession
from .repository import RestockRepository
from .service import RestockService
from ..products.dependencies import ProductServiceDep


def get_restock_repository(session: DBSession) -> RestockRepository:
    return RestockRepository(session)


def get_restock_service(
    session: DBSession,
    service_product: ProductServiceDep,
    repo: RestockRepository = Depends(get_restock_repository),
) -> RestockService:
    return RestockService(session=session, repo=repo, service_product=service_product)


RestockServiceDep = Annotated[RestockService, Depends(get_restock_service)]
