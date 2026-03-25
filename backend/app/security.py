from __future__ import annotations

import datetime as dt
import uuid

import jwt
from passlib.context import CryptContext

from .settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(*, user_id: uuid.UUID, channel: str, username: str | None = None) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    exp = now + dt.timedelta(minutes=settings.jwt_expires_minutes)
    payload = {
        "sub": str(user_id),
        "channel": channel,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    if username:
        payload["username"] = username
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
