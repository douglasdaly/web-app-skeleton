# -*- coding: utf-8 -*-
"""
Common functionality for API endpoints.
"""
import typing as tp

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app import schema
from app.core import security
from app.core.config import settings
from app.crud.base import (
    IUnitOfWork,
    models,
)
from app.crud.core import create_uow

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/login/access-token",
)


def get_uow() -> tp.Generator[None, IUnitOfWork, None]:
    """Yields a new :obj:`UnitOfWork` object to use.

    Yields
    ------
    UnitOfWork
        The new unit-of-work instance to use.

    """
    try:
        uow = create_uow()
        yield uow
    finally:
        uow.close()


async def get_current_user(
    uow: IUnitOfWork = Depends(get_uow),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    """Gets the current user from their token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = schema.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = uow.user.get(uid=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Gets the current (active) user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_super_user(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """Gets the current (active) super user."""
    if not (current_user.is_superuser or current_user.is_admin):
        raise HTTPException(status_code=400, detail="Not enough privileges")
    return current_user


def get_current_active_admin(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """Gets the current (active) admin user."""
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="Not enough privileges")
    return current_user


class get_current_active_user_with_roles:
    """
    Gets the current (active) user with the specified role(s).
    """

    def __init__(self, *roles: str, match_all: bool = False) -> None:
        self.roles = roles
        self.match_all = match_all

    def __call__(
        self,
        current_user: models.User = Depends(get_current_active_user)
    ) -> models.User:
        if current_user.is_admin:
            return current_user

        user_roles = (x.name for x in current_user.roles)
        op = all if self.match_all else any
        if not op(x in user_roles for x in self.roles):
            raise HTTPException(
                status_code=400,
                detail="Not enough privileges",
            )
        return current_user
