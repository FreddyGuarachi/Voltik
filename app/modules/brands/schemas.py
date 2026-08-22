import uuid
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class BrandBase(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    origen: str = Field(min_length=2, max_length=30)
    provider: str = Field(min_length=2, max_length=30)
    is_active: bool = Field(default=True)


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=30)
    origen: str | None = Field(default=None, min_length=2, max_length=30)
    provider: str | None = Field(default=None, min_length=2, max_length=30)
    is_active: bool | None = Field(default=None)


class BrandResponse(BrandBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BrandQuery(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=50)

    name: str | None = Field(default=None, min_length=2, max_length=30)
    origen: str | None = Field(default=None, min_length=2, max_length=30)
    provider: str | None = Field(default=None, min_length=2, max_length=30)
    is_active: bool | None = Field(default=None)

    order_by: Literal["name", "origen", "provider", "is_active"] = Field(default="name")
    order_dir: Literal["asc", "desc"] = "asc"


class BrandResponseList(BaseModel):
    items: list[BrandResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
