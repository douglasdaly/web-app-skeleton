# -*- coding: utf-8 -*-
"""
SQLAlchemy (declarative) base Model class to use.
"""
import typing as tp
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.types import TypeEngine
from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr,
)

from app.crud.models.base import ModelBase
from app.drivers.sqlalchemy.utils import GUID
from app.utils.strutils import camel_to_snake


_ASSOCIATION_TABLES: tp.Dict[tp.Tuple[str, str], sa.Table] = {}


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


def get_association_table(
    left: tp.Union[str, Base],
    right: tp.Union[str, Base],
    name: tp.Optional[str] = None,
    *,
    left_column: str = 'id',
    right_column: str = 'id',
    left_type: tp.Type[TypeEngine] = sa.Integer,
    right_type: tp.Type[TypeEngine] = sa.Integer,
) -> sa.Table:
    """Gets the association table for many-to-many relationships.

    This will either generate a new table, or if it's already been
    created, return the existing instance from the global cache.

    Parameters
    ----------
    left : Union[str, Base]
        The first table (or :obj:`Base` from which the table name can be
        gotten) for the association.
    right : Union[str, Base]
        The second table (or :obj:`Base` from which the table name can
        be gotten) for the association.
    name : str, optional
        The name of the new association table to use (if not provided a
        name will be generated, it's recommended to allow the name to be
        autogenerated, unless there's a compelling reason not to).
    left_column : str, optional
        The column name from the `left` table to use for the association
        ID (default is ``id``).
    right_column : str, optional
        The column name from the `right` table to use for the
        association ID (default is ``id``).
    left_type : sa.TypeEngine, optional
        The SQLAlchemy data type of the `left_column` (default is
        :obj:`sa.Integer`).
    right_type : sa.TypeEngine, optional
        The SQLAlchemy data type of the `right_column` (default is
        :obj:`sa.Integer`).

    Returns
    -------
    sa.Table
        The SQLAlchemy association table to use.

    """
    global _ASSOCIATION_TABLES

    if isinstance(left, Base):
        l_nm = Base.__tablename__
    else:
        l_nm = left
    if isinstance(right, Base):
        r_nm = Base.__tablename__
    else:
        r_nm = right

    key = (l_nm, r_nm)
    if key in _ASSOCIATION_TABLES:
        return _ASSOCIATION_TABLES[key]

    if name is None:
        name = f"asc_{left}_to_{right}"

    a_tbl = sa.Table(
        name,
        Base.metadata,
        sa.Column(
            'left_id',
            left_type,
            sa.ForeignKey(f"{left}.{left_column}"),
        ),
        sa.Column(
            'right_id',
            right_type,
            sa.ForeignKey(f"{right}.{right_column}"),
        ),
    )

    _ASSOCIATION_TABLES[key] = a_tbl

    return a_tbl
