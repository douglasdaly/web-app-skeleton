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
from app.schema.role import Role


# Base class
class UserBase(BaseSchemaJS):
    """
    Shared base class for User schema.
    """
    pass


# - Create
class UserCreate(UserBase):
    """
    Schema for creating users.
    """
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_admin: bool = False
    name: tp.Optional[NameCreate] = None
    roles: tp.List[str] = []


# - Update
class UserUpdate(UserBase):
    """
    Schema for updating users.
    """
    email: tp.Optional[EmailStr] = None
    password: tp.Optional[str] = None
    is_active: tp.Optional[bool] = None
    is_superuser: tp.Optional[bool] = None
    is_admin: tp.Optional[bool] = None
    name: tp.Optional[tp.Union[NameCreate, NameUpdate]] = None
    roles: tp.Optional[tp.List[str]] = None


# Storage base schema
class UserBaseStored(UserBase):
    """
    Schema for stored users.
    """
    uid: tp.Optional[UUID] = None
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_admin: bool
    name: tp.Optional[Name] = None
    roles: tp.List[Role] = []

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
