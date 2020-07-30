# -*- coding: utf-8 -*-
"""
Name object storage repository specification.
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
from app.crud.models.name import NameType
from app.schema.name import (
    NameCreate,
    NameUpdate,
)


class NameRepository(Repository, tp.Protocol):
    """
    Interface for NameRepository objects.
    """

    def get_by_last(self, last_name: str) -> tp.List[NameType]:
        ...

    def get_by_first(self, first_name: str) -> tp.List[NameType]:
        ...

    def get_by_full(
        self,
        first_name: str,
        last_name: str,
    ) -> tp.List[NameType]:
        ...


class NameRepositoryBase(
    RepositoryBase[NameType, NameCreate, NameUpdate],
    metaclass=ABCMeta,
):
    """
    Name object storage repository base class.
    """

    @abstractmethod
    def get_by_last(self, last_name: str) -> tp.List[NameType]:
        """Gets the name(s) with the given `last_name`.

        Parameters
        ----------
        last_name : str
            The last name of the Name object(s) to get.

        Returns
        -------
        List[NameType]
            Any name(s) with the matching `last_name` given.

        """
        pass

    @abstractmethod
    def get_by_first(self, first_name: str) -> tp.List[NameType]:
        """Gets the name(s) with the given `first_name`.

        Parameters
        ----------
        first_name : str
            The first name of the Name object(s) to get.

        Returns
        -------
        List[NameType]
            Any name(s) with the matching `first_name` given.

        """
        pass

    @abstractmethod
    def get_by_full(
        self,
        first_name: str,
        last_name: str,
    ) -> tp.List[NameType]:
        """Gets the name(s) with the given `first_name` and `last_name`.

        Parameters
        ----------
        first_name : str
            The first name of the Name object(s) to get.
        last_name : str
            The last name of the Name object(s) to get.

        Returns
        -------
        List[NameType]
            Any name(s) with the matching `first_name` and `last_name`
            given.

        """
        pass
