# -*- coding: utf-8 -*-
"""
SQLAlchemy (declarative) base Model class to use.
"""
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr,
)

from app.crud.models.base import ModelBase
from app.drivers.sqlalchemy.utils import GUID
from app.utils.strutils import camel_to_snake


@as_declarative()
class Base(ModelBase):
    """
    SQLAlchemy declarative base class to use.
    """
    __name__: str

    id = sa.Column('id', sa.Integer, primary_key=True)
    uid = sa.Column(GUID, unique=True, index=True, default=uuid4)

    @declared_attr
    def __tablename__(cls) -> str:
        if (ret := camel_to_snake(cls.__name__)).endswith('s'):
            return f"{ret}es"
        return f"{ret}s"


metadata = sa.MetaData()
