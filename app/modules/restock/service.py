from sqlalchemy.ext.asyncio import AsyncSession

from .repository import RestockRepository
from .schemas import RestockCreate
from .models import Restock
from ..products.service import ProductService


class RestockService:
    def __init__(
        self,
        session: AsyncSession,
        repo: RestockRepository,
        service_product: ProductService,
    ):
        self.session = session
        self.repo = repo
        self.service_product = service_product

    async def create(self, restock: RestockCreate) -> Restock:
        await self.service_product.add_stock(
            product_id=restock.product_id, quantity=restock.quantity
        )

        restock = await self.repo.create(restock)

        await self.session.commit()
        await self.session.refresh(restock)

        return restock
