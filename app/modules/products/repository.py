import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Product
from .schemas import ProductCreate, ProductQuery, ProductUpdate
from app.core.pagination import count_items, apply_order, paginate


class ProductRepository:
    ORDER_FIELD = {
        "sku": Product.sku,
        "stock": Product.stock,
        "is_active": Product.is_active,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: ProductCreate) -> Product:
        product_db = Product(**product.model_dump())
        self.session.add(product_db)

        return product_db

    async def find_all(self, query: ProductQuery) -> dict:
        stmt = select(Product)

        if query.sku:
            stmt = stmt.where(Product.sku.ilike(f"%{query.sku}%"))
        if query.stock is not None:
            stmt = stmt.where(Product.stock == query.stock)
        if query.is_active is not None:
            stmt = stmt.where(Product.is_active == query.is_active)

        total = await count_items(stmt=stmt, session=self.session)

        stmt = apply_order(
            stmt=stmt,
            column=self.ORDER_FIELD[query.order_by],
            order_dir=query.order_dir,
        )

        stmt = paginate(stmt=stmt, skip=query.skip, limit=query.limit)

        items = (await self.session.scalars(stmt)).all()

        return {"items": items, "total": total}

    async def find_by_id(self, product_id: uuid.UUID) -> Product:
        brand_db = select(Product).where(Product.id == product_id)

        return await self.session.scalar(brand_db)

    async def find_by_sku(self, product: str) -> Product:
        brand_db = select(Product).where(Product.sku == product)

        return await self.session.scalar(brand_db)

    async def update(self, product: Product, product_data: ProductUpdate) -> Product:
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
