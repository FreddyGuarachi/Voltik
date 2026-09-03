import uuid
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

from .models import UserRole


class UserBase(BaseModel):
    user_name: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=4, max_length=20)
    is_active: bool = True
    role: UserRole


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    user_name: str | None = Field(default=None, min_length=4, max_length=20)
    password: str | None = Field(default=None, min_length=4, max_length=20)
    is_active: bool | None = None
    role: UserRole | None = None


class UserResponse(BaseModel):
    id: uuid.UUID
    user_name: str
    is_active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserQuery(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=50)

    user_name: str | None = Field(default=None, min_length=4, max_length=20)
    is_active: bool | None = None
    role: UserRole | None = None

    order_by: Literal["user_name", "is_active", "role"] = "user_name"
    order_dir: Literal["asc", "desc"] = "asc"


class UserResponseList(BaseModel):
    items: list[UserResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
