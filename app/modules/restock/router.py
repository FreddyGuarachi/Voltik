from fastapi import APIRouter, status, Depends

from .dependencies import RestockServiceDep
from .schemas import RestockResponse, RestockCreate, DailySummary
from ..auth.dependencies import get_current_user

router = APIRouter(
    prefix="/restock", tags=["Restock"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=RestockResponse, status_code=status.HTTP_201_CREATED)
async def create(restock_in: RestockCreate, service: RestockServiceDep):
    return await service.create(restock_in)


@router.get("/summary", response_model=list[DailySummary])
async def get_daily_summary(service: RestockServiceDep):
    return await service.get_daily_summary()
