import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate, ProductQuery, ProductUpdate
from app.modules.products.repository import ProductRepository
from app.modules.products.service import ProductService
from app.modules.sales.models import Sale
from app.core.exceptions import (
    AlreadyExistsException,
    InsufficientStockError,
    NotFoundException,
)


@pytest.mark.asyncio
class TestProductRepository:
    async def test_find_all(
        self,
        db_session: AsyncSession,
        product_repo: ProductRepository,
        product_in: ProductCreate,
    ):
        await product_repo.create(product_in)
        await db_session.commit()

        query = ProductQuery(
            sku=product_in.sku,
            stock=product_in.stock,
            is_active=product_in.is_active,
            brand_id=product_in.brand_id,
            order_by="sku",
            order_dir="asc",
            skip=0,
            limit=10,
        )

        result = await product_repo.find_all(query)

        assert "items" in result
        assert "total" in result
        assert len(result["items"]) > 0
        assert result["total"] > 0

    async def test_delete_hard(
        self,
        db_session: AsyncSession,
        product: Product,
        product_repo: ProductRepository,
    ):
        await product_repo.delete(product)
        await db_session.commit()

        deleted_product = await product_repo.find_by_id(product.id)
        assert deleted_product is None

    async def test_delete_soft(
        self,
        db_session: AsyncSession,
        product: Product,
        product_repo: ProductRepository,
        sale: Sale,
    ):
        await product_repo.delete(product)
        await db_session.commit()

        updated_product = await product_repo.find_by_id(product.id)
        assert updated_product is not None
        assert updated_product.is_active is False


@pytest.mark.asyncio
class TestProductService:
    async def test_reduce_stock(
        self,
        db_session: AsyncSession,
        product_service: ProductService,
        product: Product,
    ):
        await product_service.reduce_stock(product.id, quantity=4)
        await db_session.refresh(product)

        assert product.stock == 6

    async def test_reduce_stock_exact_amount(
        self,
        db_session: AsyncSession,
        product_service: ProductService,
        product: Product,
    ):
        await product_service.reduce_stock(product.id, quantity=product.stock)
        await db_session.refresh(product)

        assert product.stock == 0

    async def test_reduce_stock_insufficient(
        self, product_service: ProductService, product: Product
    ):
        with pytest.raises(InsufficientStockError):
            await product_service.reduce_stock(product.id, quantity=product.stock + 1)

    async def test_add_stock(
        self,
        db_session: AsyncSession,
        product_service: ProductService,
        product: Product,
    ):
        await product_service.add_stock(product.id, quantity=5)
        await db_session.refresh(product)

        assert product.stock == 15

    async def test_create_duplicate_sku(
        self, product_service: ProductService, product_in: ProductCreate
    ):
        await product_service.create(product_in)

        with pytest.raises(AlreadyExistsException):
            await product_service.create(product_in)

    async def test_create_brand_not_found(
        self, product_service: ProductService, product_in: ProductCreate
    ):
        product_in.brand_id = uuid.uuid4()

        with pytest.raises(NotFoundException):
            await product_service.create(product_in)

    async def test_find_by_id_not_found(self, product_service: ProductService):
        product_id = uuid.uuid4()

        with pytest.raises(NotFoundException):
            await product_service.find_by_id(product_id)

    async def test_update_duplicate_sku(
        self,
        product_service: ProductService,
        product: Product,
        product_in: ProductCreate,
    ):
        product_in.sku = "SKU2"
        other_product = await product_service.create(product_in)

        product_data = ProductUpdate(sku=other_product.sku)

        with pytest.raises(AlreadyExistsException):
            await product_service.update(product.id, product_data)

    async def test_update_brand_not_found(
        self, product_service: ProductService, product: Product
    ):
        product_data = ProductUpdate(brand_id=uuid.uuid4())

        with pytest.raises(NotFoundException):
            await product_service.update(product.id, product_data)
