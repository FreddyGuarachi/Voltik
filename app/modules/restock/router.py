from fastapi import APIRouter, status

from .dependencies import RestockServiceDep
from .schemas import RestockResponse, RestockCreate

router = APIRouter(prefix="/restock", tags=["Restock"])


@router.post("/", response_model=RestockResponse, status_code=status.HTTP_201_CREATED)
async def create(restock: RestockCreate, service: RestockServiceDep):
    return await service.create(restock)
