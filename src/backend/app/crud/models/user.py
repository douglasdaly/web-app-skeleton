# -*- coding: utf-8 -*-
"""
Interface for User storage model.
"""
import typing as tp

from pydantic import EmailStr

from app.crud.models.base import Model, ModelBase
from app.crud.models.name import Name, NameBase

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
    hashed_password: str
