import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserUpdate, UserQuery, UserResponseList
from .repository import UserRepository
from app.core.exceptions import AlreadyExistsException


class UserService:
    def __init__(self, session: AsyncSession, repo: UserRepository):
        self.session = session
        self.repo = repo

    async def get_user_or_raise(self, user_id: uuid.UUID) -> User:
        user = await self.repo.find_by_id(user_id)

        if user is None:
            raise AlreadyExistsException("User", user_id)

        return user

    async def create(self, user: UserCreate) -> User:
        existing_user_name = await self.repo.find_by_user_name(user.user_name)

        if existing_user_name:
            raise AlreadyExistsException("User", user.user_name)

        user = User(
            user_name=user.user_name,
            password_hash=user.password,
            is_active=user.is_active,
            role=user.role,
        )

        user = await self.repo.create(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def find_all(self, query: UserQuery) -> UserResponseList:
        result = await self.repo.find_all(query)

        return UserResponseList(**result)

    async def find_by_id(self, user_id: uuid.UUID) -> User:
        return await self.get_user_or_raise(user_id)

    async def find_by_user_name(self, user_name: str) -> User:
        user_name = await self.repo.find_by_user_name(user_name)

        if user_name is None:
            raise AlreadyExistsException("User", user_name.user_name)

        return user_name

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        user = await self.get_user_or_raise(user_id)

        await self.repo.update(user=user, user_data=user_data)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, user_id: uuid.UUID) -> None:
        user = await self.get_user_or_raise(user_id)

        await self.repo.delete(user)
        await self.session.commit()
