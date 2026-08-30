from fastapi import APIRouter, status

from .dependencies import SaleServiceDep
from .schemas import SalesResponse, SaleCreate

router = APIRouter(prefix="/sale", tags=["Sales"])


@router.post("/", response_model=SalesResponse, status_code=status.HTTP_201_CREATED)
async def create(sale: SaleCreate, service: SaleServiceDep):
    return await service.create(sale)
