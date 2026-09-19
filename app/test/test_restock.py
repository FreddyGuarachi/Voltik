import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.models import Product
from app.modules.restock.models import Restock
from app.modules.restock.repository import RestockRepository
from app.modules.restock.schemas import RestockCreate
from app.modules.restock.service import RestockService


@pytest.mark.asyncio
class TestRestockRepository:
    async def test_get_daily_summary(
        self,
        db_session: AsyncSession,
        restock_repo: RestockRepository,
        restock: Restock,
    ):
        result = await restock_repo.get_daily_summary()

        assert len(result) == 1
        assert result[0].total_quantity == restock.quantity


@pytest.mark.asyncio
class TestRestockService:
    async def test_create_increases_stock(
        self,
        db_session: AsyncSession,
        restock_service: RestockService,
        product: Product,
        restock_in: RestockCreate,
    ):
        await restock_service.create(restock_in)
        await db_session.refresh(product)

        assert product.stock == 15
