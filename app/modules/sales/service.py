from sqlalchemy.ext.asyncio import AsyncSession

from .models import Sale
from .repository import SaleRepository
from .schemas import SaleCreate
from ..products.service import ProductService


class SaleService:
    def __init__(
        self,
        session: AsyncSession,
        repo: SaleRepository,
        product_service: ProductService,
    ):
        self.session = session
        self.repo = repo
        self.product_service = product_service

    async def create(self, sale: SaleCreate) -> Sale:
        await self.product_service.reduce_stock(sale.product_id, sale.quantity)

        sale = await self.repo.create(sale)

        await self.session.commit()
        await self.session.refresh(sale)

        return sale
