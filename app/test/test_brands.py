import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.brands.models import Brand
from app.modules.brands.schemas import BrandCreate, BrandUpdate
from app.modules.brands.repository import BrandRepository
from app.modules.brands.service import BrandService
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate
from app.core.exceptions import AlreadyExistsException, NotFoundException


@pytest.mark.asyncio
async def test_create(
    db_session: AsyncSession, repo: BrandRepository, brand_in: BrandCreate
):
    await repo.create(brand_in)
    await db_session.commit()

    stmt = select(Brand).where(Brand.name == "Bosch")
    result = await db_session.scalar(stmt)

    assert result.name == "Bosch"
    assert result.origin == "Alemania"


@pytest.mark.asyncio
async def test_create_duplicate(service: BrandService, brand_in: BrandCreate):
    await service.create(brand_in)

    with pytest.raises(AlreadyExistsException):
        await service.create(brand_in)


@pytest.mark.asyncio
async def test_find_by_id(
    db_session: AsyncSession, repo: BrandRepository, brand_in: BrandCreate
):
    brand = await repo.create(brand_in)
    await db_session.commit()

    stmt = await repo.find_by_id(brand.id)

    assert stmt is not None
    assert stmt.name == "Bosch"


@pytest.mark.asyncio
async def test_find_by_id_not_found(service: BrandService):
    brand_id = uuid.uuid4()

    with pytest.raises(NotFoundException):
        await service.find_by_id(brand_id)


@pytest.mark.asyncio
async def test_update(
    db_session: AsyncSession, repo: BrandRepository, brand_in: BrandCreate
):
    brand = await repo.create(brand_in)
    await db_session.commit()

    brand_data = BrandUpdate(name="Willard", origin="Argentina")

    result = await repo.update(brand=brand, brand_data=brand_data)

    assert result.name == "Willard"
    assert result.origin == "Argentina"


@pytest.mark.asyncio
async def test_update_duplicate(brand_in: BrandCreate, service: BrandService):
    brand = await service.create(brand_in)

    brand_another = BrandCreate(
        name="Moura", origin="Brasil", provider="Moura", is_active=True
    )
    await service.create(brand_another)

    brand_data = BrandUpdate(name="Moura")

    with pytest.raises(AlreadyExistsException):
        await service.update(brand_id=brand.id, brand_data=brand_data)


@pytest.mark.asyncio
async def test_delete_soft_repo(
    db_session: AsyncSession,
    repo: BrandRepository,
    product_in: ProductCreate,
    product_repo: ProductRepository,
    brand: Brand,
):
    await product_repo.create(product_in)
    await db_session.commit()

    result = await repo.delete(brand)

    assert result is True
    assert brand.is_active is False


@pytest.mark.asyncio
async def test_delete_hard_repo(
    db_session: AsyncSession, repo: BrandRepository, brand_in: BrandCreate
):
    brand = await repo.create(brand_in)
    await db_session.commit()

    assert await repo.delete(brand) is False


@pytest.mark.asyncio
async def test_delete_soft_service(
    db_session: AsyncSession,
    service: BrandService,
    product_in: ProductCreate,
    product_repo: ProductRepository,
    brand: Brand,
):
    await product_repo.create(product_in)
    await db_session.commit()

    await service.delete(brand.id)
    await db_session.refresh(brand)

    assert brand.is_active is False


@pytest.mark.asyncio
async def test_delete_not_found_service(service: BrandService):
    brand_id = uuid.uuid4()

    with pytest.raises(NotFoundException):
        await service.delete(brand_id)


@pytest.mark.asyncio
async def test_delete_soft_cascade_service(
    db_session: AsyncSession,
    service: BrandService,
    product_in: ProductCreate,
    brand: Brand,
    product_repo: ProductRepository,
):
    product = await product_repo.create(product_in)
    await db_session.commit()

    await service.delete(brand.id)

    assert brand.is_active is False
    assert product.is_active is False


@pytest.mark.asyncio
async def test_delete_hard_no_cascade_service(
    service: BrandService,
    brand: Brand,
    repo: BrandRepository,
):
    await service.delete(brand.id)

    brand_deleted = await repo.find_by_id(brand.id)

    assert brand_deleted is None
