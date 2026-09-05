import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload

from .models import Product
from .schemas import ProductCreate, ProductQuery, ProductUpdate
from app.core.pagination import count_items, apply_order, paginate
from ..sales.models import Sale
from ..restock.models import Restock


class ProductRepository:
    ORDER_FIELD = {
        "sku": Product.sku,
        "stock": Product.stock,
        "is_active": Product.is_active,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: ProductCreate) -> Product:
        product = Product(**product.model_dump())
        self.session.add(product)

        return product

    async def find_all(self, query: ProductQuery) -> dict:
        stmt = select(Product).options(joinedload(Product.brand))

        if query.sku:
            stmt = stmt.where(Product.sku.ilike(f"%{query.sku}%"))
        if query.stock is not None:
            stmt = stmt.where(Product.stock == query.stock)
        if query.is_active is not None:
            stmt = stmt.where(Product.is_active == query.is_active)
        if query.brand_id is not None:
            stmt = stmt.where(Product.brand_id == query.brand_id)

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

    async def find_by_id(self, product_id: uuid.UUID) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(joinedload(Product.brand))
        )

        return await self.session.scalar(stmt)

    async def find_by_sku(self, product_sku: str) -> Product | None:
        stmt = select(Product).where(Product.sku == product_sku)

        return await self.session.scalar(stmt)

    async def update(self, product: Product, product_data: ProductUpdate) -> Product:
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        return product

    async def has_movements(self, product_id: uuid.UUID) -> bool:
        stmt = select(
            exists().where(Sale.product_id == product_id)
            | exists().where(Restock.product_id == product_id)
        )
        return await self.session.scalar(stmt)

    async def delete(self, product: Product) -> None:
        if await self.has_movements(product.id):
            product.is_active = False
            return

        await self.session.delete(product)
