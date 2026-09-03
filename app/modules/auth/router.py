from fastapi import APIRouter

from .schemas import Token
from .dependencies import AuthServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/", response_model=Token)
async def login(user_name: str, password: str, service: AuthServiceDep):
    return await service.login(user_name=user_name, password=password)
