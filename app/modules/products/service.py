import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product
from .schemas import ProductCreate, ProductQuery, ProductResponseList, ProductUpdate
from .repository import ProductRepository
from app.core.exceptions import (
    NotFoundException,
    AlreadyExistsException,
    InsufficientStockError,
)
from ..brands.service import BrandService


class ProductService:
    def __init__(
        self,
        session: AsyncSession,
        repo: ProductRepository,
        brand_service: BrandService,
    ):
        self.session = session
        self.repo = repo
        self.brand_service = brand_service

    async def create(self, product: ProductCreate) -> Product:
        await self.brand_service.find_by_id(product.brand_id)

        existing_sku = await self.repo.find_by_sku(product.sku)

        if existing_sku:
            raise AlreadyExistsException("Product", product.sku)

        product = await self.repo.create(product)

        await self.session.commit()
        await self.session.refresh(product)

        await product.awaitable_attrs.brand
        return product

    async def find_all(self, query: ProductQuery) -> dict:
        return await self.repo.find_all(query)

    async def find_by_id(self, product_id: uuid.UUID) -> Product:
        product = await self.repo.find_by_id(product_id)

        if product is None:
            raise NotFoundException("Product", product_id)

        return product

    async def update(
        self, product_id: uuid.UUID, product_data: ProductUpdate
    ) -> Product:
        product = await self.find_by_id(product_id)

        if product_data.brand_id is not None:
            await self.brand_service.find_by_id(product_data.brand_id)

        await self.repo.update(product=product, product_data=product_data)
        await self.session.commit()
        await self.session.refresh(product)

        await product.awaitable_attrs.brand
        return product

    async def delete(self, product_id: uuid.UUID) -> None:
        product = await self.find_by_id(product_id)

        await self.repo.delete(product)
        await self.session.commit()

    async def reduce_stock(self, product_id: uuid.UUID, quantity: int) -> None:
        product = await self.find_by_id(product_id)

        if product.stock < quantity:
            raise InsufficientStockError("Product", product.stock)

        stock = product.stock - quantity
        product_data = ProductUpdate(stock=stock)

        return await self.repo.update(product=product, product_data=product_data)

    async def add_stock(self, product_id: uuid.UUID, quantity: int) -> None:
        product = await self.find_by_id(product_id)

        stock = product.stock + quantity
        product_data = ProductUpdate(stock=stock)

        return await self.repo.update(product=product, product_data=product_data)
