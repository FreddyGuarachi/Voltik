import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BrandCreate, BrandQuery, BrandResponseList, BrandUpdate
from .repository import BrandRepository
from .models import Brand


class BrandService:
    def __init__(self, session: AsyncSession, repo: BrandRepository):
        self.session = session
        self.repo = repo

    async def create(self, brand: BrandCreate) -> Brand:
        brand_db = await self.repo.find_by_name(brand.name)

        if brand_db:
            raise Exception

        brand_db = await self.repo.create(brand)
        await self.session.commit()
        await self.session.refresh(brand_db)

        return brand_db

    async def find_all(self, query: BrandQuery) -> BrandResponseList:
        result = await self.repo.find_all(query)

        return BrandResponseList(**result)

    async def find_by_id(self, brand_id: uuid.UUID) -> Brand:
        brand_db = await self.repo.find_by_id(brand_id)

        if brand_db is None:
            raise Exception

        return brand_db

    async def update(self, brand_id: uuid.UUID, brand_data: BrandUpdate) -> Brand:
        brand = await self.repo.find_by_id(brand_id)

        if brand is None:
            raise Exception

        result = await self.repo.update(brand=brand, brand_data=brand_data)
        await self.session.commit()
        await self.session.refresh(result)

        return result

    async def delete(self, brand_id: uuid.UUID) -> None:
        brand = await self.repo.find_by_id(brand_id)

        if brand is None:
            raise Exception

        await self.repo.delete(brand)
        await self.session.commit()
