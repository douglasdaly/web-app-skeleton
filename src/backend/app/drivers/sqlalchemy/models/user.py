# -*- coding: utf-8 -*-
"""
User storage schema for SQLAlchemy.
"""
import typing as tp

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.crud.models.user import UserBase
from app.drivers.sqlalchemy.models.base import Base

if tp.TYPE_CHECKING:
    from app.drivers.sqlalchemy.models.name import Name  # noqa: F401


class User(UserBase, Base):
    """
    Storage table for User objects in SQLAlchemy.
    """
    email = sa.Column(sa.String, unique=True, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)

    name_id = sa.Column(sa.Integer, sa.ForeignKey('names.id'))
    name = relationship("Name")

    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    is_admin = sa.Column(sa.Boolean, default=False, nullable=False)
