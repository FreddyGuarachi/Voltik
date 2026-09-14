import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.base import Base
from app.modules.brands.models import Brand
from app.modules.brands.schemas import BrandCreate
from app.modules.brands.repository import BrandRepository
from app.modules.brands.service import BrandService
from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate
from app.modules.products.repository import ProductRepository

engine = create_async_engine("sqlite+aiosqlite:///:memory:")


@pytest_asyncio.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
def brand_in() -> BrandCreate:
    return BrandCreate(
        name="Bosch", origin="Alemania", provider="Bosch Argentina", is_active=True
    )


@pytest_asyncio.fixture
async def brand(db_session: AsyncSession, brand_in: BrandCreate) -> Brand:
    repo = BrandRepository(db_session)
    brand = await repo.create(brand_in)
    await db_session.commit()
    return brand


@pytest_asyncio.fixture
def product_in(brand: Brand) -> ProductCreate:
    return ProductCreate(
        sku="SKU1",
        stock=10,
        capacity_ah=60,
        capacity_cca=500,
        voltage=12,
        is_active=True,
        brand_id=brand.id,
    )


@pytest_asyncio.fixture
async def product(db_session: AsyncSession, product_in: ProductCreate) -> Product:
    repo = ProductRepository(db_session)
    product = await repo.create(product_in)
    await db_session.commit()
    return product


@pytest_asyncio.fixture
async def repo(db_session: AsyncSession) -> BrandRepository:
    return BrandRepository(db_session)


@pytest_asyncio.fixture
async def product_repo(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(db_session)


@pytest_asyncio.fixture
async def service(
    db_session: AsyncSession,
    repo: ProductRepository,
    product_repo: ProductRepository,
) -> BrandService:
    return BrandService(session=db_session, repo=repo, product_repo=product_repo)
