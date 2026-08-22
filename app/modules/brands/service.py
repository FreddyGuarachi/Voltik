from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BrandCreate, BrandQuery, BrandResponseList
from .repository import BrandRepository
from .models import Brand


class BrandService:
    def __init__(self, session: AsyncSession, repo: BrandRepository):
        self.session = session
        self.repo = repo

    async def create(self, brand: BrandCreate) -> Brand:
        brand_db = await self.repo.create(brand)
        await self.session.commit()
        await self.session.refresh(brand_db)

        return brand_db

    async def find_all(self, query: BrandQuery) -> BrandResponseList:
        return await self.repo.find_all(query)
