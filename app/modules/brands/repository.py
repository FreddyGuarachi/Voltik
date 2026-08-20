from sqlalchemy.ext.asyncio import AsyncSession
from .models import Brand
from .schemas import BrandCreate


class BrandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, brand: BrandCreate) -> Brand:
        new_brand = Brand(**brand.model_dump())

        self.session.add(new_brand)
        await self.session.commit()
        await self.session.refresh(new_brand)

        return new_brand
