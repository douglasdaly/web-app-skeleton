# -*- coding: utf-8 -*-
"""
Role object storage repository specification.
"""
from abc import (
    ABCMeta,
    abstractmethod,
)
import typing as tp

from app.crud.repos.base import (
    Repository,
    RepositoryBase,
)
from app.crud.models.role import RoleType
from app.schema.role import (
    RoleCreate,
    RoleUpdate,
)


class RoleRepository(Repository, tp.Protocol):
    """
    Interface for UserRepository objects.
    """

    def get_by_name(self, name: str) -> tp.Optional[RoleType]:
        ...


class RoleRepositoryBase(
    RepositoryBase[RoleType, RoleCreate, RoleUpdate],
    metaclass=ABCMeta,
):
    """
    Role object storage repository base class.
    """

    @abstractmethod
    def get_by_name(self, name: str) -> tp.Optional[RoleType]:
        """Gets the role object with the given `name`.

        Parameters
        ----------
        name : str
            The name of the role to get the role object for.

        Returns
        -------
        Optional[RoleType]
            The role object with the given `name` (if it exists).

        """
        pass
