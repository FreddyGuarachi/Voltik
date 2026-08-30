from sqlalchemy.ext.asyncio import AsyncSession

from .models import Sale
from .schemas import SaleCreate


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sale: SaleCreate) -> Sale:
        sale = Sale(**sale.model_dump())
        self.session.add(sale)

        return sale
