import uuid
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .service import AuthService
from ..users.dependencies import UserServiceDep
from ..users.models import User
from app.core.security import decode_access_token
from app.core.exceptions import UserNotActiveError, ForbiddenError

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_service(user_service: UserServiceDep) -> AuthService:
    return AuthService(user_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    user_service: UserServiceDep, token: str = Depends(oauth2_schema)
) -> User:
    payload = decode_access_token(token)

    user = await user_service.find_by_id(uuid.UUID(payload.get("sub")))

    if not user.is_active:
        raise UserNotActiveError()

    return user


async def get_current_admin(token: str = Depends(oauth2_schema)) -> None:
    payload = decode_access_token(token)

    if payload.get("role") != "admin":
        raise ForbiddenError()
