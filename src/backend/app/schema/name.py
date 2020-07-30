# -*- coding: utf-8 -*-
"""
Name schema.
"""
import typing as tp
from uuid import UUID

from app.schema.base import BaseSchemaJS


class NameBase(BaseSchemaJS):
    """
    Name schema base class.
    """
    title: tp.Optional[str] = None
    middle: tp.Optional[str] = None
    suffix: tp.Optional[str] = None
    preferred: tp.Optional[str] = None


class NameCreate(NameBase):
    """
    Schema for creating Name models.
    """
    first: str
    last: str


class NameUpdate(NameBase):
    """
    Schema for updating Name models.
    """
    first: tp.Optional[str] = None
    last: tp.Optional[str] = None


class Name(NameBase):
    """
    Schema for representing Name models.
    """
    uid: tp.Optional[UUID] = None
    first: str
    last: str

    class Config:
        orm_mode = True


class NameStored(Name):
    """
    Storage schema for Name models.
    """
    pass
