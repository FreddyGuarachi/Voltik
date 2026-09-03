from typing import Annotated
from fastapi import Depends

from .service import AuthService
from ..users.dependencies import UserServiceDep


def get_auth_service(user_service: UserServiceDep) -> AuthService:
    return AuthService(user_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
