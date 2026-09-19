import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.models import Product
from app.modules.sales.models import Sale
from app.modules.sales.repository import SaleRepository
from app.modules.sales.schemas import SaleCreate
from app.modules.sales.service import SaleService
from app.core.exceptions import InsufficientStockError


@pytest.mark.asyncio
class TestSaleRepository:
    async def test_get_daily_summary(
        self, db_session: AsyncSession, sale_repo: SaleRepository, sale: Sale
    ):
        result = await sale_repo.get_daily_summary()

        assert len(result) == 1
        assert result[0].total_quantity == sale.quantity


@pytest.mark.asyncio
class TestSaleService:
    async def test_create_reduces_stock(
        self,
        db_session: AsyncSession,
        sale_service: SaleService,
        product: Product,
        sale_in: SaleCreate,
    ):
        await sale_service.create(sale_in)
        await db_session.refresh(product)

        assert product.stock == 5

    async def test_create_insufficient_stock(
        self,
        sale_service: SaleService,
        product: Product,
        sale_in: SaleCreate,
    ):
        sale_in.quantity = product.stock + 1

        with pytest.raises(InsufficientStockError):
            await sale_service.create(sale_in)
