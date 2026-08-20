import uuid
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
    provider: str | None = Field(min_length=2, max_length=30)
    is_active: bool | None = Field(default=None)


class BrandResponse(BrandBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
