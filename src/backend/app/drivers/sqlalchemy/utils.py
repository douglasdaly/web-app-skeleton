# -*- coding: utf-8 -*-
"""
Utilities for the SQLAlchemy driver.
"""
import os
import typing as tp
from urllib import parse
import uuid

from sqlalchemy import (
    create_engine,
    event,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Engine
from sqlalchemy.types import (
    CHAR,
    TypeDecorator,
    TypeEngine,
)


class GUID(TypeDecorator):
    """
    Platform-independent GUID type for SQLAlchemy.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect: tp.Any) -> TypeEngine:
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgresql.UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(
        self,
        value: tp.Any,
        dialect: tp.Any,
    ) -> tp.Optional[str]:
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value).hex
        return value.hex

    def process_result_value(
        self,
        value: tp.Any,
        dialect: tp.Any,
    ) -> tp.Optional[uuid.UUID]:
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value


def create_db_uri(
    dialect: str,
    db_name: tp.Optional[str] = None,
    *,
    driver: tp.Optional[str] = None,
    user: tp.Optional[str] = None,
    password: tp.Optional[str] = None,
    host: tp.Optional[str] = None,
    port: tp.Optional[int] = None,
    **kwargs: tp.Any,
) -> str:
    """Creates the SQLAlchemy database URI string to use.

    Parameters
    ----------
    dialect : str
        The dialect of the engine to create the URI for (e.g. 'sqlite').
    db_name : str, optional
        The name of the database to connect to (if any).
    driver : str, optional
        The database driver to use for connections.
    user : str, optional
        The username to use for authenticating the database connection.
    password : str, optional
        The password to use for authenticating the database connection.
    host : str, optional
        The host name/address of the database to connect to.
    port : int, optional
        The port number on the `host` to connect to the database on.
    kwargs : optional
        Any additional keyword arguments to append as query parameters
        to the returned URI string.

    Returns
    -------
    str
        The full database URI connection string to use.

    """
    db_uri = dialect
    if driver:
        db_uri += f"[+{driver}]"
    db_uri += "://"
    if user:
        db_uri += user
        if password:
            db_uri += f":{password}"
        if host:
            db_uri += "@"
    if host:
        db_uri += host
        if port:
            db_uri += f":{port}"
    if db_name:
        if dialect == 'sqlite' and os.path.isabs(db_name):
            db_uri += db_name
        else:
            db_uri += f"/{db_name}"
    if kwargs:
        if not db_uri.endswith('/'):
            db_uri += "/"
        db_uri += '?' + parse.urlencode(kwargs, doseq=True)
    return db_uri


def get_schema() -> tp.Set[str]:
    """Gets the additional model schema from the SQLAlchemy metadata.

    Returns
    -------
    Set[str]
        The set of additional schema specified by the models.

    """
    from app.drivers.sqlalchemy.models import base

    return set(
        x.schema for x in base.metadata.tables.values()
        if x.schema is not None
    )


def build_engine(db_uri: str, **kwargs: tp.Any) -> Engine:
    """Creates and configures a new SQLAlchemy database engine.

    Parameters
    ----------
    db_uri : str
        The full database connection URI to use for the connection.
    **kwargs : optional
        Any additional keyword arguments to pass through to the
        ``create_engine`` function.

    Returns
    -------
    Engine
        The newly created and configured SQLAlchemy database engine to
        use.

    """
    engine = create_engine(db_uri, **kwargs)

    if engine.dialect.name == 'sqlite':
        # - Add Schema handling to SQLite connections
        schema_map = {x: f"{x}.sqlite3" for x in get_schema()}

        @event.listens_for(engine, 'connect')
        def _sqlite_connect(dbapi_conn: tp.Any, rec: tp.Any) -> None:
            for sname, fname in schema_map.items():
                dbapi_conn.execute(f"ATTACH DATABASE '{fname}' AS '{sname}'")
            return

    return engine
