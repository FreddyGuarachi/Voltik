import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User
from .schemas import UserCreate, UserQuery, UserUpdate
from app.core.pagination import count_items, apply_order, paginate


class UserRepository:
    ORDER_FIELD = {
        "user_name": User.user_name,
        "is_active": User.is_active,
        "role": User.role,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        self.session.add(user)

        return user

    async def find_all(self, query: UserQuery) -> dict:
        stmt = select(User)

        if query.user_name:
            stmt = stmt.where(User.user_name.ilike(f"%{query.user_name}%"))

        if query.is_active is not None:
            stmt = stmt.where(User.is_active == query.is_active)

        if query.role:
            stmt = stmt.where(User.role == query.role)

        total = await count_items(stmt=stmt, session=self.session)

        stmt = apply_order(
            stmt=stmt,
            column=self.ORDER_FIELD[query.order_by],
            order_dir=query.order_dir,
        )

        stmt = paginate(stmt=stmt, skip=query.skip, limit=query.limit)

        result = await self.session.scalars(stmt)
        items = result.all()

        return {"items": items, "total": total}

    async def find_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)

        return await self.session.scalar(stmt)

    async def find_by_user_name(self, user_name: str) -> User | None:
        stmt = select(User).where(User.user_name == user_name)

        return await self.session.scalar(stmt)

    async def update(self, user: User, user_data: UserUpdate) -> User:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        return user

    async def delete(self, user: User) -> None:
        return await self.session.delete(user)
