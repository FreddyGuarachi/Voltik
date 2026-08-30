import uuid
from pydantic import BaseModel, Field, ConfigDict


class SaleBase(BaseModel):
    quantity: int = Field(default=1, ge=1, le=20)
    product_id: uuid.UUID


class SaleCreate(SaleBase):
    pass


class SalesResponse(SaleBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
