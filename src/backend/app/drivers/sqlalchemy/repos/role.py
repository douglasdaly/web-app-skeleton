# -*- coding: utf-8 -*-
"""
Role CRUD-based storage repository for SQLAlchemy driver.
"""
import typing as tp

from sqlalchemy import asc

from app.crud.repos.role import RoleRepositoryBase
from app.drivers.sqlalchemy.crud import SQLRepositoryMixin
from app.drivers.sqlalchemy.models.role import Role


class RoleRepository(SQLRepositoryMixin, RoleRepositoryBase[Role]):
    """
    SQLAlchemy-based CRUD storage repository for Role objects.
    """
    __order_by__ = {
        'name': asc,
    }

    def get_by_name(self, name: str) -> tp.Optional[Role]:
        return self.uow.db.query(self.model) \
            .filter(self.model.name == name.lower()) \
            .first()
