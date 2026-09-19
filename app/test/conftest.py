import pytest
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
from app.modules.products.service import ProductService
from app.modules.sales.models import Sale
from app.modules.sales.schemas import SaleCreate
from app.modules.sales.repository import SaleRepository
from app.modules.sales.service import SaleService
from app.modules.restock.models import Restock
from app.modules.restock.schemas import RestockCreate
from app.modules.restock.repository import RestockRepository
from app.modules.restock.service import RestockService
from app.modules.users.models import User, UserRole
from app.modules.users.schemas import UserCreate
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.modules.auth.service import AuthService

engine = create_async_engine("sqlite+aiosqlite:///:memory:")


@pytest_asyncio.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        yield session


# --- Brand fixtures ---


@pytest.fixture
def brand_in() -> BrandCreate:
    return BrandCreate(
        name="Bosch", origin="Alemania", provider="Bosch Argentina", is_active=True
    )


@pytest_asyncio.fixture
async def brand_repo(db_session: AsyncSession) -> BrandRepository:
    return BrandRepository(db_session)


@pytest_asyncio.fixture
async def brand(
    db_session: AsyncSession, brand_repo: BrandRepository, brand_in: BrandCreate
) -> Brand:
    brand = await brand_repo.create(brand_in)
    await db_session.commit()
    return brand


@pytest_asyncio.fixture
async def brand_service(
    db_session: AsyncSession,
    brand_repo: BrandRepository,
    product_repo: ProductRepository,
) -> BrandService:
    return BrandService(session=db_session, repo=brand_repo, product_repo=product_repo)


# --- Product fixtures ---


@pytest_asyncio.fixture
async def product_repo(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(db_session)


@pytest.fixture
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
async def product(
    db_session: AsyncSession, product_repo: ProductRepository, product_in: ProductCreate
) -> Product:
    product = await product_repo.create(product_in)
    await db_session.commit()
    return product


@pytest_asyncio.fixture
async def product_service(
    db_session: AsyncSession,
    product_repo: ProductRepository,
    brand_service: BrandService,
) -> ProductService:
    return ProductService(
        session=db_session, repo=product_repo, brand_service=brand_service
    )


# --- Sale fixtures ---


@pytest.fixture
def sale_in(product: Product) -> SaleCreate:
    return SaleCreate(quantity=5, product_id=product.id)


@pytest_asyncio.fixture
async def sale_repo(db_session: AsyncSession) -> SaleRepository:
    return SaleRepository(db_session)


@pytest_asyncio.fixture
async def sale(
    db_session: AsyncSession, sale_repo: SaleRepository, sale_in: SaleCreate
) -> Sale:
    sale = await sale_repo.create(sale_in)
    await db_session.commit()
    return sale


@pytest_asyncio.fixture
async def sale_service(
    db_session: AsyncSession,
    sale_repo: SaleRepository,
    product_service: ProductService,
) -> SaleService:
    return SaleService(
        session=db_session, repo=sale_repo, product_service=product_service
    )


# --- Restock fixtures ---


@pytest.fixture
def restock_in(product: Product) -> RestockCreate:
    return RestockCreate(quantity=5, product_id=product.id)


@pytest_asyncio.fixture
async def restock_repo(db_session: AsyncSession) -> RestockRepository:
    return RestockRepository(db_session)


@pytest_asyncio.fixture
async def restock(
    db_session: AsyncSession,
    restock_repo: RestockRepository,
    restock_in: RestockCreate,
) -> Restock:
    restock = await restock_repo.create(restock_in)
    await db_session.commit()
    return restock


@pytest_asyncio.fixture
async def restock_service(
    db_session: AsyncSession,
    restock_repo: RestockRepository,
    product_service: ProductService,
) -> RestockService:
    return RestockService(
        session=db_session, repo=restock_repo, service_product=product_service
    )


# --- User fixtures ---


@pytest.fixture
def user_in() -> UserCreate:
    return UserCreate(
        user_name="freddy", password="Pass1234", is_active=True, role=UserRole.SELLER
    )


@pytest_asyncio.fixture
async def user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


@pytest_asyncio.fixture
async def user_service(db_session: AsyncSession, user_repo: UserRepository) -> UserService:
    return UserService(session=db_session, repo=user_repo)


@pytest_asyncio.fixture
async def user(user_service: UserService, user_in: UserCreate) -> User:
    return await user_service.create(user_in)


# --- Auth fixtures ---


@pytest_asyncio.fixture
async def auth_service(user_service: UserService) -> AuthService:
    return AuthService(user_service)
