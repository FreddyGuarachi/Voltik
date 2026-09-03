from app.core.exceptions import InvalidCredentialsError
from app.core.security import verify_password
from ..users.service import UserService


class AuthService:
    def __init__(self, user_service: UserService) -> dict:
        self.user_service = user_service

    async def login(self, user_name: str, password: str):
        user = await self.user_service.find_by_user_name(user_name)

        is_password_valid = verify_password(
            password=password, hashed_password=user.password_hash
        )

        if not is_password_valid:
            raise InvalidCredentialsError()

        return {"sub": user.user_name}
