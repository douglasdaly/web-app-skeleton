# -*- coding: utf-8 -*-
"""
Core functionality for the SQLAlchemy storage driver.
"""
from app.core.config import settings
from app.drivers.sqlalchemy import (
    models,
    repos,
)
from app.drivers.sqlalchemy.models.base import Base
from app.drivers.sqlalchemy.crud import UnitOfWork
from app.drivers.sqlalchemy.session import (
    engine,
    SessionLocal,
)
from app.schema import UserCreate

__all__ = [
    'create_uow',
    'models',
    'repos',
    'setup_storage',
    'storage_ready',
    'UnitOfWork',
]


def storage_ready() -> bool:
    """Checks if the storage system is ready for use.

    Returns
    -------
    bool
        Whether or not the storage system is ready for use.

    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return True
    except Exception:
        raise
    finally:
        db.close()


def create_uow() -> UnitOfWork:
    """Creates a new SQLAlchemy-based :obj:`UnitOfWork` to use.

    Returns
    -------
    UnitOfWork
        The (SQLAlchemy-based) unit-of-work object to use.

    """
    try:
        db_session = SessionLocal()
        return UnitOfWork(db_session)
    finally:
        db_session.close()


def setup_storage() -> None:
    """Sets up the storage system for the first time running."""
    Base.metadata.create_all(bind=engine)

    uow = create_uow()
    user = uow.user.get_by_email(settings.FIRST_ADMIN_USER)
    if not user:
        new_user = UserCreate(
            email=settings.FIRST_ADMIN_USER,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_superuser=True,
            is_admin=True,
        )
        with uow:
            user = uow.user.create(obj_in=new_user)


def init_storage() -> None:
    """Initializes the storage system for use on each application start.
    """
    pass
