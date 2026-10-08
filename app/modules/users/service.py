import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, UserRole
from .schemas import UserCreate, UserUpdate, UserQuery, UserResponseList
from .repository import UserRepository
from app.core.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    InvalidCredentialsError,
    SelfLockoutError,
)
from app.core.security import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession, repo: UserRepository):
        self.session = session
        self.repo = repo

    async def create(self, user_in: UserCreate) -> User:
        existing_user_name = await self.repo.find_by_user_name(user_in.user_name)

        if existing_user_name:
            raise AlreadyExistsException("User", user_in.user_name)

        hashed_password = get_password_hash(user_in.password)

        user = User(
            user_name=user_in.user_name,
            password_hash=hashed_password,
            is_active=user_in.is_active,
            role=user_in.role,
        )

        user = await self.repo.create(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def find_all(self, query: UserQuery) -> UserResponseList:
        result = await self.repo.find_all(query)

        return UserResponseList(**result)

    async def find_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.repo.find_by_id(user_id)

        if user is None:
            raise NotFoundException("User", user_id)

        return user

    async def find_by_user_name(self, user_name: str) -> User:
        user = await self.repo.find_by_user_name(user_name)

        if user is None:
            raise InvalidCredentialsError()

        return user

    async def update(
        self, user_id: uuid.UUID, user_data: UserUpdate, current_user_id: uuid.UUID
    ) -> User:
        user = await self.find_by_id(user_id)

        if user.id == current_user_id:
            is_deactivating = user_data.is_active is False
            is_demoting = user_data.role == UserRole.SELLER

            if is_deactivating or is_demoting:
                raise SelfLockoutError()

        if user_data.password is not None:
            user.password_hash = get_password_hash(user_data.password)

        await self.repo.update(user=user, user_data=user_data)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, user_id: uuid.UUID, current_user_id: uuid.UUID) -> None:
        user = await self.find_by_id(user_id)

        if user.id == current_user_id:
            raise SelfLockoutError()

        await self.repo.delete(user)
        await self.session.commit()
