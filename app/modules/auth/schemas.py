from pydantic import BaseModel

from ..users.models import UserRole


class Token(BaseModel):
    access_token: str
    role: UserRole
    token_type: str = "bearer"
