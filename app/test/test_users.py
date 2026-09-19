import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserQuery, UserUpdate
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.core.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    InvalidCredentialsError,
)


@pytest.mark.asyncio
class TestUserRepository:
    async def test_find_all(
        self,
        user_repo: UserRepository,
        user_in: UserCreate,
        user: User,
    ):
        query = UserQuery(
            user_name=user.user_name,
            is_active=user_in.is_active,
            role=user_in.role,
            order_by="user_name",
            order_dir="asc",
            skip=0,
            limit=10,
        )

        result = await user_repo.find_all(query)

        assert "items" in result
        assert "total" in result
        assert len(result["items"]) > 0
        assert result["total"] > 0

    async def test_find_by_user_name(self, user_repo: UserRepository, user: User):
        result = await user_repo.find_by_user_name(user.user_name)

        assert result is not None
        assert result.id == user.id

    async def test_update(self, user_repo: UserRepository, user: User):
        user_data = UserUpdate(user_name="nuevo_nombre")

        result = await user_repo.update(user=user, user_data=user_data)

        assert result.user_name == "nuevo_nombre"

    async def test_delete(
        self, db_session: AsyncSession, user_repo: UserRepository, user: User
    ):
        await user_repo.delete(user)
        await db_session.commit()

        deleted_user = await user_repo.find_by_id(user.id)
        assert deleted_user is None


@pytest.mark.asyncio
class TestUserService:
    async def test_create_duplicate_user_name(
        self, user_service: UserService, user_in: UserCreate
    ):
        await user_service.create(user_in)

        with pytest.raises(AlreadyExistsException):
            await user_service.create(user_in)

    async def test_find_by_id_not_found(self, user_service: UserService):
        user_id = uuid.uuid4()

        with pytest.raises(NotFoundException):
            await user_service.find_by_id(user_id)

    async def test_find_by_user_name_not_found(self, user_service: UserService):
        with pytest.raises(InvalidCredentialsError):
            await user_service.find_by_user_name("no_existe")

    async def test_update_user_name(self, user_service: UserService, user: User):
        user_data = UserUpdate(user_name="cambiado")

        result = await user_service.update(user.id, user_data)

        assert result.user_name == "cambiado"

    async def test_delete(
        self,
        user_service: UserService,
        user_repo: UserRepository,
        user: User,
    ):
        await user_service.delete(user.id)

        deleted_user = await user_repo.find_by_id(user.id)
        assert deleted_user is None
