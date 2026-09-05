import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, AlreadyExistsException
from .schemas import BrandCreate, BrandQuery, BrandUpdate
from .repository import BrandRepository
from .models import Brand


class BrandService:
    def __init__(self, session: AsyncSession, repo: BrandRepository):
        self.session = session
        self.repo = repo

    async def create(self, brand: BrandCreate) -> Brand:
        existing_name = await self.repo.find_by_name(brand.name)

        if existing_name:
            raise AlreadyExistsException("Brand", brand.name)

        brand = await self.repo.create(brand)

        await self.session.commit()
        await self.session.refresh(brand)

        return brand

    async def find_all(self, query: BrandQuery) -> dict:
        return await self.repo.find_all(query)

    async def find_by_id(self, brand_id: uuid.UUID) -> Brand:
        brand = await self.repo.find_by_id(brand_id)

        if brand is None:
            raise NotFoundException("Brand", brand_id)

        return brand

    async def update(self, brand_id: uuid.UUID, brand_data: BrandUpdate) -> Brand:
        brand = await self.find_by_id(brand_id)

        if brand_data.name is not None:
            existing_name = await self.repo.find_by_name(brand_data.name)

            if existing_name and existing_name.id != brand_id:
                raise AlreadyExistsException("Brand", brand.name)

        await self.repo.update(brand=brand, brand_data=brand_data)
        await self.session.commit()
        await self.session.refresh(brand)

        return brand

    async def delete(self, brand_id: uuid.UUID) -> None:
        brand = await self.find_by_id(brand_id)

        await self.repo.delete(brand)
        await self.session.commit()
