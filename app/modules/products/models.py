import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import UUID, Integer, Float, String, Boolean, func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.modules.brands.models import Brand


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    capacity_ah: Mapped[int] = mapped_column(Integer)
    capacity_cca: Mapped[int] = mapped_column(Integer)
    voltage: Mapped[float] = mapped_column(Float, default=12)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )

    id_brand: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("brands.id")
    )
    brand: Mapped["Brand"] = relationship(back_populates="products")
