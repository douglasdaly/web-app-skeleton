# -*- coding: utf-8 -*-
"""
User CRUD-based storage repository for SQLAlchemy driver.
"""
import typing as tp

from app.crud.repos.user import UserRepositoryBase
from app.drivers.sqlalchemy.crud import SQLRepositoryMixin
from app.drivers.sqlalchemy.models.user import User


class UserRepository(SQLRepositoryMixin, UserRepositoryBase[User]):
    """
    SQLAlchemy-based CRUD storage repository for User objects.
    """

    def get_by_email(self, email: str) -> tp.Optional[User]:
        return self.uow.db.query(self.model) \
            .filter(self.model.email == email) \
            .first()
