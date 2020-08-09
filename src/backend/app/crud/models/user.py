# -*- coding: utf-8 -*-
"""
Interface for User storage model.
"""
import typing as tp

from pydantic import EmailStr

from app.crud.models.base import Model, ModelBase
from app.crud.models.name import Name, NameBase
from app.crud.models.role import Role, RoleBase

UserType = tp.TypeVar('UserType', bound='UserBase')


class User(Model, tp.Protocol):
    """
    Interface for User objects.
    """
    email: EmailStr
    name: tp.Optional[Name]
    is_active: bool
    is_superuser: bool
    is_admin: bool
    roles: tp.List[Role]
    hashed_password: str


class UserBase(ModelBase):
    """
    Base class for user objects.
    """
    email: EmailStr
    name: tp.Optional[NameBase]
    is_active: bool
    is_superuser: bool
    is_admin: bool
    roles: tp.List[RoleBase]
    hashed_password: str
