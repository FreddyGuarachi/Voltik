import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from .models import Brand
from .schemas import BrandCreate, BrandQuery, BrandUpdate
from app.core.pagination import count_items, apply_order, paginate
from ..products.models import Product


class BrandRepository:
    ORDER_FIELD = {
        "name": Brand.name,
        "origen": Brand.origin,
        "provider": Brand.provider,
        "is_active": Brand.is_active,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, brand: BrandCreate) -> Brand:
        brand = Brand(**brand.model_dump())
        self.session.add(brand)

        return brand

    async def find_all(self, query: BrandQuery) -> dict:
        stmt = select(Brand)

        # Filter.
        if query.name:
            stmt = stmt.where(Brand.name.ilike(f"%{query.name}%"))
        if query.origin:
            stmt = stmt.where(Brand.origin.ilike(f"%{query.origin}%"))
        if query.provider:
            stmt = stmt.where(Brand.provider.ilike(f"%{query.provider}%"))
        if query.is_active is not None:
            stmt = stmt.where(Brand.is_active == query.is_active)

        # Count items.
        total = await count_items(stmt=stmt, session=self.session)

        # Order by.
        stmt = apply_order(
            stmt=stmt,
            column=self.ORDER_FIELD[query.order_by],
            order_dir=query.order_dir,
        )

        # Paginate.
        stmt = paginate(stmt=stmt, skip=query.skip, limit=query.limit)

        # Execute query.
        result = await self.session.scalars(stmt)
        items = result.all()

        return {"items": items, "total": total}

    async def find_by_id(self, brand_id: uuid.UUID) -> Brand | None:
        stmt = select(Brand).where(Brand.id == brand_id)

        return await self.session.scalar(stmt)

    async def find_by_name(self, brand: str) -> Brand | None:
        stmt = select(Brand).where(Brand.name == brand)

        return await self.session.scalar(stmt)

    async def update(self, brand: Brand, brand_data: BrandUpdate) -> Brand:
        for key, value in brand_data.model_dump(exclude_unset=True).items():
            setattr(brand, key, value)

        return brand

    async def delete(self, brand: Brand) -> bool:
        if await self.has_products(brand.id):
            brand.is_active = False
            return True

        await self.session.delete(brand)
        return False

    async def has_products(self, brand_id: uuid.UUID) -> bool:
        stmt = select(exists().where(Product.brand_id == brand_id))
        return await self.session.scalar(stmt)
