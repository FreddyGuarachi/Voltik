import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from .schemas import ProductCreate, ProductQuery, ProductResponseList, ProductUpdate
from .repository import ProductRepository
from app.core.exceptions import NotFoundException, AlreadyExistsException


class ProductService:
    def __init__(self, session: AsyncSession, repo: ProductRepository):
        self.session = session
        self.repo = repo

    async def _get_product_or_raise(self, product_id: uuid.UUID) -> Product:
        product_db = await self.repo.find_by_id(product_id)

        if product_db is None:
            raise NotFoundException("Product", "id", product_id)

        return product_db

    async def create(self, product: ProductCreate) -> Product:
        product_db = await self.repo.find_by_sku(product.sku)

        if product_db:
            raise AlreadyExistsException("Product", "sku", product.sku)

        product_db = await self.repo.create(product)
        await self.session.commit()
        await self.session.refresh(product_db)

        return product_db

    async def find_all(self, query: ProductQuery) -> ProductResponseList:
        result = await self.repo.find_all(query)

        return ProductResponseList(**result)

    async def find_by_id(self, product_id: uuid.UUID) -> Product:
        return await self._get_product_or_raise(product_id)

    async def update(
        self, product_id: uuid.UUID, product_data: ProductUpdate
    ) -> Product:
        product = await self._get_product_or_raise(product_id)

        await self.repo.update(product=product, product_data=product_data)
        await self.session.commit()
        await self.session.refresh(product)

        return product

    async def delete(self, product_id: uuid.UUID) -> None:
        product = await self._get_product_or_raise(product_id)

        await self.repo.delete(product)
        await self.session.commit()
