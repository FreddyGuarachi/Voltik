import pytest

from app.core.security import decode_access_token
from app.core.exceptions import InvalidCredentialsError
from app.modules.auth.service import AuthService
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate


@pytest.mark.asyncio
class TestAuthService:
    async def test_login_success(
        self, auth_service: AuthService, user_in: UserCreate, user: User
    ):
        result = await auth_service.login(
            user_name=user.user_name, password=user_in.password
        )

        assert "access_token" in result

        payload = decode_access_token(result["access_token"])
        assert payload["sub"] == str(user.id)
        assert payload["role"] == user.role

    async def test_login_wrong_password(self, auth_service: AuthService, user: User):
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login(user_name=user.user_name, password="wrong_pass")

    async def test_login_user_not_found(self, auth_service: AuthService):
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login(user_name="ghost", password="whatever")
