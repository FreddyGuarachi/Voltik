from fastapi import APIRouter

from .schemas import BrandCreate
from .dependencies import BrandServiceDep

router = APIRouter(prefix="/brand", tags=["brand"])


@router.post("/")
async def create(brand: BrandCreate, service: BrandServiceDep):
    return await service.create(brand)
