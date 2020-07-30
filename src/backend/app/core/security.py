# -*- coding: utf-8 -*-
"""
Security functionality for the API.
"""
from datetime import (
    datetime,
    timedelta,
)
import typing as tp

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: tp.Any,
    expires_delta: tp.Optional[timedelta] = None,
) -> str:
    """Creates a new access token to use."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    data = {
        "exp": expire,
        "sub": str(subject)
    }
    encoded = jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_password(password: str, hashed: str) -> bool:
    """Verifies the given password matches the hashed version."""
    return pwd_context.verify(password, hashed)


def get_password_hash(password: str) -> str:
    """Gets the hash for the given plaintext password."""
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    """Generates a password reset token."""
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = (now + delta).timestamp()
    encoded_jwt = jwt.encode(
        {
            "exp": expires,
            "nbf": now,
            "sub": email,
        },
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> tp.Optional[str]:
    """Verifies the given password reset token."""
    try:
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return decoded["email"]
    except jwt.JWTError:
        return None
