from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Brand
from .schemas import BrandCreate, BrandQuery
from app.core.pagination import count_items, apply_order, paginate


class BrandRepository:
    ORDER_FIELD = {
        "name": Brand.name,
        "origen": Brand.origen,
        "provider": Brand.provider,
        "is_active": Brand.is_active,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, brand: BrandCreate) -> Brand:
        brand_db = Brand(**brand.model_dump())
        self.session.add(brand_db)

        return brand_db

    async def find_all(self, query: BrandQuery) -> dict:
        stmt = select(Brand)

        # Filter.
        if query.name:
            stmt = stmt.where(Brand.name.ilike(f"%{query.name}%"))
        if query.origen:
            stmt = stmt.where(Brand.origen.ilike(f"%{query.origen}%"))
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
        items = (await self.session.scalars(stmt)).all()

        return {"items": items, "total": total}
