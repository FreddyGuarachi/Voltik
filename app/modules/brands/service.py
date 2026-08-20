from .schemas import BrandCreate
from .repository import BrandRepository
from .models import Brand


class BrandService:
    def __init__(self, repo: BrandRepository):
        self.repo = repo

    async def create(self, brand: BrandCreate) -> Brand:
        return await self.repo.create(brand)
