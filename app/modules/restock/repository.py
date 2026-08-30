from sqlalchemy.ext.asyncio import AsyncSession

from .models import Restock
from .schemas import RestockCreate


class RestockRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, restock: RestockCreate) -> Restock:
        restock = Restock(**restock.model_dump())
        self.session.add(restock)

        return restock
