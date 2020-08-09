# -*- coding: utf-8 -*-
"""
Role storage schema for SQLAlchemy.
"""
import typing as tp

import sqlalchemy as sa

from app.crud.models.role import RoleBase
from app.drivers.sqlalchemy.models.base import Base


class Role(RoleBase, Base):
    """
    Storage table for Role objects in SQLAlchemy.
    """
    name = sa.Column(sa.String, unique=True, index=True)
    description = sa.Column(sa.Text, nullable=True)
