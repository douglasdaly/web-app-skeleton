# -*- coding: utf-8 -*-
"""
User CRUD-based storage repository for SQLAlchemy driver.
"""
import typing as tp

import sqlalchemy as sa

from app.crud.repos.user import UserRepositoryBase
from app.drivers.sqlalchemy.crud import SQLRepositoryMixin
from app.drivers.sqlalchemy.models.user import User


class UserRepository(SQLRepositoryMixin, UserRepositoryBase[User]):
    """
    SQLAlchemy-based CRUD storage repository for User objects.
    """
    __order_by__ = {
        'email': sa.asc,
    }

    def get_by_email(self, email: str) -> tp.Optional[User]:
        return self.uow.db.query(self.model) \
            .filter(self.model.email == email) \
            .first()

    def get_by_role(
        self,
        role: tp.Optional[
            tp.Union[
                str,
                tp.Tuple[str, ...],
                tp.List[tp.Union[str, tp.Tuple[str, ...]]],
            ]
        ],
        *,
        skip: int = 0,
        limit: tp.Optional[int] = 100,
    ) -> tp.List[User]:
        if role is None:
            ret = self.uow.db.query(self.model) \
                .filter(len(self.model.roles) == 0) \
                .order_by(self.model.email)
            if skip:
                ret = ret.offset(skip)
            if limit:
                ret = ret.limit(limit)
            return ret.all()

        roles = self._helper_format_roles(role)

        qry = self.uow.db.query(self.model) \
            .join(self.model.roles)

        return []
