import jwt
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta

from .config import setting
from .exceptions import TokenExpiredError, InvalidTokenError

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload["exp"] = expire

    return jwt.encode(payload, setting.SECRET_KEY, algorithm=setting.ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
