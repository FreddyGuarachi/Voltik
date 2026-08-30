import uuid
from pydantic import BaseModel, Field, ConfigDict


class RestockBase(BaseModel):
    quantity: int = Field(default=1, ge=1, le=20)
    product_id: uuid.UUID


class RestockCreate(RestockBase):
    pass


class RestockResponse(BaseModel):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
