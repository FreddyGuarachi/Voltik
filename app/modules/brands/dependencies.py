from typing import Annotated
from fastapi import Depends

from app.core.dependencies import DBSession
from .repository import BrandRepository
from .service import BrandService
from .schemas import BrandQuery


def get_brand_repository(session: DBSession) -> BrandRepository:
    return BrandRepository(session)


def get_brand_service(
    session: DBSession,
    repo: BrandRepository = Depends(get_brand_repository),
) -> BrandService:
    return BrandService(session, repo)


BrandServiceDep = Annotated[BrandService, Depends(get_brand_service)]

BrandQueryDep = Annotated[BrandQuery, Depends()]
