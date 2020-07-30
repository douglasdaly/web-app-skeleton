# -*- coding: utf-8 -*-
"""
User schema.
"""
import typing as tp
from uuid import UUID

from pydantic import EmailStr

from app.schema.base import BaseSchemaJS
from app.schema.name import (
    Name,
    NameCreate,
    NameUpdate,
)


# Base class
class UserBase(BaseSchemaJS):
    """
    Shared base class for User schema.
    """
    email: tp.Optional[EmailStr] = None
    is_active: tp.Optional[bool] = True
    is_superuser: bool = False
    is_admin: bool = False


# - Create
class UserCreate(UserBase):
    """
    Schema for creating users.
    """
    email: EmailStr
    password: str
    name: tp.Optional[NameCreate] = None


# - Update
class UserUpdate(UserBase):
    """
    Schema for updating users.
    """
    password: tp.Optional[str] = None
    name: tp.Optional[NameUpdate] = None


# Storage base schema
class UserBaseStored(UserBase):
    """
    Schema for stored users.
    """
    uid: tp.Optional[UUID] = None
    name: tp.Optional[Name] = None

    class Config:
        orm_mode: bool = True


# - Get
class User(UserBaseStored):
    """
    Schema for users.
    """
    pass


# - Storage
class UserStored(UserBaseStored):
    """
    Schema for stored users.
    """
    hashed_password: str
