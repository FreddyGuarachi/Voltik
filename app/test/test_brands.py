import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.brands.models import Brand
from app.modules.brands.schemas import BrandCreate, BrandQuery, BrandUpdate
from app.modules.brands.repository import BrandRepository
from app.modules.brands.service import BrandService
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate
from app.core.exceptions import AlreadyExistsException, NotFoundException


@pytest.mark.asyncio
class TestBrandRepository:
    async def test_find_all(
        self,
        db_session: AsyncSession,
        brand_repo: BrandRepository,
        brand_in: BrandCreate,
    ):
        await brand_repo.create(brand_in)
        await db_session.commit()

        query = BrandQuery(
            name=brand_in.name,
            origin=brand_in.origin,
            provider=brand_in.provider,
            is_active=brand_in.is_active,
            order_by="name",
            order_dir="asc",
            skip=0,
            limit=10,
        )

        result = await brand_repo.find_all(query)

        assert "items" in result
        assert "total" in result
        assert len(result["items"]) > 0
        assert result["total"] > 0

    async def test_update(
        self,
        db_session: AsyncSession,
        brand_repo: BrandRepository,
        brand_in: BrandCreate,
    ):
        brand = await brand_repo.create(brand_in)
        await db_session.commit()

        brand_data = BrandUpdate(name="Willard", origin="Argentina")

        result = await brand_repo.update(brand=brand, brand_data=brand_data)

        assert result.name == "Willard"
        assert result.origin == "Argentina"

    async def test_delete_soft(
        self,
        db_session: AsyncSession,
        brand_repo: BrandRepository,
        product_in: ProductCreate,
        product_repo: ProductRepository,
        brand: Brand,
    ):
        await product_repo.create(product_in)
        await db_session.commit()

        result = await brand_repo.delete(brand)

        assert result is True
        assert brand.is_active is False

    async def test_delete_hard(
        self,
        db_session: AsyncSession,
        brand_repo: BrandRepository,
        brand_in: BrandCreate,
    ):
        brand = await brand_repo.create(brand_in)
        await db_session.commit()

        assert await brand_repo.delete(brand) is False


@pytest.mark.asyncio
class TestBrandService:
    async def test_create_duplicate(
        self, brand_service: BrandService, brand_in: BrandCreate
    ):
        await brand_service.create(brand_in)

        with pytest.raises(AlreadyExistsException):
            await brand_service.create(brand_in)

    async def test_find_by_id_not_found(self, brand_service: BrandService):
        brand_id = uuid.uuid4()

        with pytest.raises(NotFoundException):
            await brand_service.find_by_id(brand_id)

    async def test_update_duplicate(
        self, brand_in: BrandCreate, brand_service: BrandService
    ):
        brand = await brand_service.create(brand_in)

        brand_another = BrandCreate(
            name="Moura", origin="Brasil", provider="Moura", is_active=True
        )
        await brand_service.create(brand_another)

        brand_data = BrandUpdate(name="Moura")

        with pytest.raises(AlreadyExistsException):
            await brand_service.update(brand_id=brand.id, brand_data=brand_data)

    async def test_delete_soft_cascade(
        self,
        db_session: AsyncSession,
        brand_service: BrandService,
        product_in: ProductCreate,
        brand: Brand,
        product_repo: ProductRepository,
    ):
        product = await product_repo.create(product_in)
        await db_session.commit()

        await brand_service.delete(brand.id)

        assert brand.is_active is False
        assert product.is_active is False

    async def test_delete_hard_no_cascade(
        self,
        brand_service: BrandService,
        brand: Brand,
        brand_repo: BrandRepository,
    ):
        await brand_service.delete(brand.id)

        brand_deleted = await brand_repo.find_by_id(brand.id)

        assert brand_deleted is None
