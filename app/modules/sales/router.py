from fastapi import APIRouter, status, Depends

from .dependencies import SaleServiceDep
from .schemas import SalesResponse, SaleCreate, DailySummary
from ..auth.dependencies import get_current_user

router = APIRouter(
    prefix="/sale", tags=["Sales"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=SalesResponse, status_code=status.HTTP_201_CREATED)
async def create(sale: SaleCreate, service: SaleServiceDep):
    return await service.create(sale)


@router.get("/summary", response_model=list[DailySummary])
async def get_daily_summary(service: SaleServiceDep):
    return await service.get_daily_summary()
