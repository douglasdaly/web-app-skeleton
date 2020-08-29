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

    def _get_role_query(
        self,
        role: tp.Optional[
            tp.Union[
                str,
                tp.Tuple[str, ...],
                tp.List[tp.Union[str, tp.Tuple[str, ...]]],
            ]
        ],
    ) -> sa.orm.query.Query:
        """Helper to get the query for role-related operations."""
        ret = self.uow.db.query(self.model)
        if role is None:
            ret = ret.filter(~self.model.roles.any())
        else:
            ret = ret.join(self.model.roles)
            roles = self._helper_format_roles(role)
            exprs = []
            for r_tup in roles:
                t_expr = []
                for r in r_tup:
                    t_expr.append(self.model.roles.contains(r))
                exprs.append(sa.and_(*t_expr))
            ret = ret.filter(sa.or_(*exprs))
        return ret

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
        ret = self._get_role_query(role).order_by(self.model.email)
        if skip:
            ret = ret.offset(skip)
        if limit:
            ret = ret.limit(limit)
        return ret.all()

    def count_by_role(
        self,
        role: tp.Optional[
            tp.Union[
                str,
                tp.Tuple[str, ...],
                tp.List[tp.Union[str, tp.Tuple[str, ...]]],
            ]
        ],
    ) -> int:
        stmt = self._get_role_query(role).subquery()
        qry = self.uow.db.query(sa.distinct(stmt.c.id))
        return qry.count()
