# -*- coding: utf-8 -*-
"""
Role schema.
"""
import typing as tp
from uuid import UUID

from app.schema.base import BaseSchemaJS


class RoleBase(BaseSchemaJS):
    """
    Base class for Role schema.
    """
    description: tp.Optional[str] = None


class RoleCreate(RoleBase):
    """
    Create schema for Role objects.
    """
    name: str


class RoleUpdate(RoleBase):
    """
    Update schema for Role objects.
    """
    name: tp.Optional[str] = None


class Role(RoleBase):
    """
    Schema for Role objects.
    """
    uid: tp.Optional[UUID] = None
    name: str

    class Config:
        orm_mode: bool = True


class RoleStored(Role):
    """
    Storage schema for Role objects.
    """
    pass
