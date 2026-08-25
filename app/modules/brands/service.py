import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, AlreadyExistsException
from .schemas import BrandCreate, BrandQuery, BrandResponseList, BrandUpdate
from .repository import BrandRepository
from .models import Brand


class BrandService:
    def __init__(self, session: AsyncSession, repo: BrandRepository):
        self.session = session
        self.repo = repo

    async def _get_brand_or_raise(self, brand_id: uuid.UUID) -> Brand:
        brand = await self.repo.find_by_id(brand_id)

        if brand is None:
            raise NotFoundException("Brand", "id", brand_id)

        return brand

    async def create(self, brand: BrandCreate) -> Brand:
        brand_db = await self.repo.find_by_name(brand.name)

        if brand_db:
            raise AlreadyExistsException("Brand", "name", brand.name)

        brand_db = await self.repo.create(brand)
        await self.session.commit()
        await self.session.refresh(brand_db)

        return brand_db

    async def find_all(self, query: BrandQuery) -> BrandResponseList:
        result = await self.repo.find_all(query)

        return BrandResponseList(**result)

    async def find_by_id(self, brand_id: uuid.UUID) -> Brand:
        return await self._get_brand_or_raise(brand_id)

    async def update(self, brand_id: uuid.UUID, brand_data: BrandUpdate) -> Brand:
        brand = await self._get_brand_or_raise(brand_id)

        await self.repo.update(brand=brand, brand_data=brand_data)
        await self.session.commit()
        await self.session.refresh(brand)

        return brand

    async def delete(self, brand_id: uuid.UUID) -> None:
        brand = await self._get_brand_or_raise(brand_id)

        await self.repo.delete(brand)
        await self.session.commit()
