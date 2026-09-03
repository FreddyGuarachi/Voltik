from typing import Annotated
from fastapi import Depends

from app.core.dependencies import DBSession
from .repository import UserRepository
from .service import UserService
from .schemas import UserQuery


def get_user_repository(session: DBSession) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    session: DBSession, repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(session=session, repo=repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

UserQueryDep = Annotated[UserQuery, Depends()]
