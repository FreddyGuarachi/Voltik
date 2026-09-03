from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Row

from .models import Restock
from .schemas import RestockCreate
from ..products.models import Product
from ..brands.models import Brand


class RestockRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, restock: RestockCreate) -> Restock:
        restock = Restock(**restock.model_dump())
        self.session.add(restock)

        return restock

    async def get_daily_summary(self) -> list[Row]:
        stmt = (
            select(
                func.date(Restock.created_at).label("date"),
                Product.sku.label("product_sku"),
                Brand.name.label("brand_name"),
                func.sum(Restock.quantity).label("total_quantity"),
            )
            .join(Product, Product.id == Restock.product_id)
            .join(Brand, Brand.id == Product.brand_id)
            .group_by(func.date(Restock.created_at), Product.sku, Brand.name)
            .order_by(func.date(Restock.created_at), Product.sku, Brand.name)
        )

        rows = await self.session.execute(stmt)

        return rows.all()
