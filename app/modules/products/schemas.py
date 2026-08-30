import uuid
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

from ..brands.schemas import BrandSummary


class ProductBase(BaseModel):
    sku: str = Field(min_length=2, max_length=50)
    stock: int = Field(default=0, ge=0)
    capacity_ah: float = Field(ge=1, le=300)
    capacity_cca: float = Field(ge=1, le=2000)
    voltage: float = Field(default=12, ge=1, le=48)
    is_active: bool = True
    brand_id: uuid.UUID


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = Field(default=None, min_length=2, max_length=50)
    stock: int | None = Field(default=None, ge=0)
    capacity_ah: float | None = Field(default=None, ge=1, le=300)
    capacity_cca: float | None = Field(default=None, ge=1, le=2000)
    voltage: float | None = Field(default=None, ge=1, le=48)
    is_active: bool | None = None
    brand_id: uuid.UUID | None = None


class ProductResponse(ProductBase):
    id: uuid.UUID
    brand: BrandSummary

    model_config = ConfigDict(from_attributes=True)


class ProductQuery(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=50)

    sku: str | None = Field(default=None, min_length=2)
    stock: int | None = Field(default=None, ge=0)
    is_active: bool | None = None
    brand_id: uuid.UUID | None = None

    order_by: Literal["sku", "stock", "is_active"] = "sku"
    order_dir: Literal["asc", "desc"] = "asc"


class ProductResponseList(BaseModel):
    items: list[ProductResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
