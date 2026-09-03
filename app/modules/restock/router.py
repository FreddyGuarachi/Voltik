from fastapi import APIRouter, status

from .dependencies import RestockServiceDep
from .schemas import RestockResponse, RestockCreate, DailySummary

router = APIRouter(prefix="/restock", tags=["Restock"])


@router.post("/", response_model=RestockResponse, status_code=status.HTTP_201_CREATED)
async def create(restock: RestockCreate, service: RestockServiceDep):
    return await service.create(restock)


@router.get("/summary", response_model=list[DailySummary])
async def get_daily_summary(service: RestockServiceDep):
    return await service.get_daily_summary()
