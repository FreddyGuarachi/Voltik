from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Row

from .models import Sale
from .schemas import SaleCreate
from ..products.models import Product
from ..brands.models import Brand


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sale: SaleCreate) -> Sale:
        sale = Sale(**sale.model_dump())
        self.session.add(sale)

        return sale

    async def get_daily_summary(self) -> list[Row]:
        stmt = (
            select(
                func.date(Sale.created_at).label("date"),
                Product.sku.label("product_sku"),
                Brand.name.label("brand_name"),
                func.sum(Sale.quantity).label("total_quantity"),
            )
            .join(Product, Product.id == Sale.product_id)
            .join(Brand, Brand.id == Product.brand_id)
            .group_by(func.date(Sale.created_at), Product.sku, Brand.name)
            .order_by(func.date(Sale.created_at), Product.sku, Brand.name)
        )

        rows = await self.session.execute(stmt)

        return rows.all()
