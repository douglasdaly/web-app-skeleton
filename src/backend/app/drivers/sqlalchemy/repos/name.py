# -*- coding: utf-8 -*-
"""
Name CRUD-based storage repository for SQLAlchemy driver.
"""
import typing as tp

from sqlalchemy import asc, desc

from app.crud.repos.name import NameRepositoryBase
from app.drivers.sqlalchemy.crud import SQLRepositoryMixin
from app.drivers.sqlalchemy.models.name import Name


class NameRepository(SQLRepositoryMixin, NameRepositoryBase[Name]):
    """
    SQLAlchemy-based CRUD storage repository for User objects.
    """
    __order_by__ = {
        'last': asc,
        'first': asc,
    }

    def get_by_first(self, first_name: str) -> tp.List[Name]:
        return self.uow.db.query(self.model) \
            .filter(self.model.first == first_name) \
            .order_by(self.model.last) \
            .all()

    def get_by_last(self, last_name: str) -> tp.List[Name]:
        return self.uow.db.query(self.model) \
            .filter(self.model.last == last_name) \
            .order_by(self.model.first) \
            .all()

    def get_by_full(
        self,
        first_name: str,
        last_name: str,
    ) -> tp.List[Name]:
        return self.uow.db.query(self.model) \
            .filter(self.model.last == last_name) \
            .filter(self.model.first == first_name) \
            .all()
