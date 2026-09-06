from sqlalchemy.ext.asyncio import AsyncSession

from .models import Sale
from .repository import SaleRepository
from .schemas import SaleCreate, DailySummary
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
        await self.product_service.reduce_stock(
            product_id=sale.product_id, quantity=sale.quantity
        )

        sale = await self.repo.create(sale)

        await self.session.commit()
        await self.session.refresh(sale)

        return sale

    async def get_daily_summary(self) -> list[DailySummary]:
        rows = await self.repo.get_daily_summary()

        return [
            DailySummary(
                date=row.date,
                product_sku=row.product_sku,
                brand_name=row.brand_name,
                total_quantity=row.total_quantity,
            )
            for row in rows
        ]
