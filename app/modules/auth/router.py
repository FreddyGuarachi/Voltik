from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Token
from .dependencies import AuthServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(
    service: AuthServiceDep, form_data: OAuth2PasswordRequestForm = Depends()
):
    return await service.login(
        user_name=form_data.username, password=form_data.password
    )
