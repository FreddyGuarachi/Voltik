from datetime import datetime, timezone, timedelta

import jwt
import pytest

from app.core.config import setting
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.core.exceptions import InvalidTokenError, TokenExpiredError


def test_get_password_hash():
    password = "123abc"

    result = get_password_hash(password)

    assert result != password


def test_verify_password():
    password = "123abc"

    hashed_password = get_password_hash(password)

    result = verify_password(password=password, hashed_password=hashed_password)

    assert result
    assert not verify_password("abc123", hashed_password)


def test_create_access_token():
    data = {"sub": "admin1", "role": "admin"}

    token = create_access_token(data)

    payload = decode_access_token(token)

    assert payload["sub"] == data["sub"]
    assert payload["role"] == data["role"]


def test_decode_access_token():
    with pytest.raises(InvalidTokenError):
        decode_access_token("invalid_token")


def test_decode_access_token_expired():
    expired = datetime.now(timezone.utc) - timedelta(minutes=1)
    payload = {"sub": "admin1", "exp": expired}

    token = jwt.encode(payload, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

    with pytest.raises(TokenExpiredError):
        decode_access_token(token)
