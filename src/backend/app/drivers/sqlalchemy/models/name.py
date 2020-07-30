# -*- coding: utf-8 -*-
"""
Name storage schema for SQLAlchemy.
"""
import sqlalchemy as sa

from app.crud.models.name import NameBase
from app.drivers.sqlalchemy.models.base import Base


class Name(NameBase, Base):
    """
    Storage table for Name objects in SQLAlchemy.
    """
    title = sa.Column(sa.String, nullable=True)
    first = sa.Column(sa.String, nullable=False, index=True)
    middle = sa.Column(sa.String, nullable=True)
    last = sa.Column(sa.String, nullable=False, index=True)
    suffix = sa.Column(sa.String, nullable=True)
    preferred = sa.Column(sa.String, nullable=True)
