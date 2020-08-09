# -*- coding: utf-8 -*-
"""
Base components for SQLAlchemy storage driver.
"""
from abc import ABCMeta
import typing as tp
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import UnitOfWorkBase
from app.crud.repos.base import (
    CreateSchemaType,
    RepositoryBase,
    UpdateSchemaType,
)
from app.drivers.sqlalchemy.models.base import Base

ModelTypeSQL = tp.TypeVar('ModelTypeSQL', bound=Base)
RepositoryTypeSQL = tp.TypeVar('RepositoryTypeSQL', bound='Repository')
UnitOfWorkTypeSQL = tp.TypeVar('UnitOfWorkTypeSQL', bound='UnitOfWork')


class SQLRepositoryMixin(object, metaclass=ABCMeta):
    """
    SQLAlchemy-based object storage repository mixin.
    """
    __order_by__: tp.Optional[tp.Dict[str, tp.Callable]] = None

    if tp.TYPE_CHECKING:
        model: tp.Type[Base]
        uow: 'UnitOfWork'

    def _save(self, obj: ModelTypeSQL) -> ModelTypeSQL:
        self.uow.db.add(obj)
        self.uow.db.flush()
        return obj

    def _load(self, uid: UUID) -> ModelTypeSQL:
        return self.uow.db.query(self.model) \
            .filter(self.model.uid == uid) \
            .first()

    def _delete(self, obj: ModelTypeSQL) -> ModelTypeSQL:
        self.uow.db.delete(obj)
        self.uow.db.flush()
        return obj

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: tp.Optional[int] = 100,
    ) -> tp.List[ModelTypeSQL]:
        ret = self.uow.db.query(self.model)
        if self.__order_by__:
            for k, v in self.__order_by__.items():
                ret = ret.order_by(v(getattr(self.model, k)))
        if skip:
            ret = ret.offset(skip)
        if limit is not None:
            ret = ret.limit(limit)
        return ret.all()


class Repository(
    SQLRepositoryMixin,
    RepositoryBase[ModelTypeSQL, CreateSchemaType, UpdateSchemaType],
):
    """
    SQLAlchemy-based CRUD object storage repository.
    """
    pass


class UnitOfWork(UnitOfWorkBase[Base, Repository]):
    """
    SQLAlchemy-based unit-of-work class.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        return super().__init__()

    def close(self) -> None:
        super().close()
        return self.db.close()

    def commit(self) -> None:
        super().commit()
        return self.db.commit()

    def rollback(self) -> None:
        super().rollback()
        return self.db.rollback()
