# -*- coding: utf-8 -*-
"""
Base components for the CRUD subpackage.
"""
from abc import abstractmethod
from contextlib import AbstractContextManager
from functools import cached_property
from types import TracebackType
import typing as tp

from app.crud import (
    models,
    repos,
)
from app.crud.models.base import ModelType
from app.crud.repos.base import RepositoryType
from app.utils.strutils import camel_to_snake

UnitOfWorkType = tp.TypeVar("UnitOfWorkType", bound="UnitOfWorkBase")


class IModels(tp.Protocol):
    """
    Interface for the dynamically-loaded ``models`` module.
    """
    __all__: tp.List[str]
    Name: tp.Type[models.NameBase]
    User: tp.Type[models.UserBase]


class IRepos(tp.Protocol):
    """
    Interface for the dynamically-loaded ``repos`` module.
    """
    Repository: tp.Type[repos.RepositoryBase]
    NameRepository: tp.Type[repos.NameRepositoryBase]
    UserRepository: tp.Type[repos.UserRepositoryBase]


class IUnitOfWork(tp.ContextManager, tp.Protocol):
    """
    Interface for the dynamically-loaded UnitOfWork object.
    """
    user: repos.UserRepository
    name: repos.NameRepository

    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class UnitOfWorkBase(
    tp.Generic[ModelType, RepositoryType],
    AbstractContextManager,
):
    """
    Unit-of-Work abstract base class.
    """
    if tp.TYPE_CHECKING:
        user: repos.UserRepository
        name: repos.NameRepository

    __models: tp.Set[tp.Type[ModelType]]

    def __init_subclass__(cls, **kwargs: tp.Any) -> None:
        cls.__models = set()

    def __init__(self) -> None:
        self._depth = 0

    def close(self) -> None:
        """Safely closes this unit of work (if needed)."""
        return

    # Context-management

    def __enter__(self) -> IUnitOfWork:
        self._depth += 1
        return self

    def __exit__(
        self,
        exc_type: tp.Optional[tp.Type[BaseException]],
        exc_val: tp.Optional[BaseException],
        exc_tb: tp.Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self._depth -= 1

    @abstractmethod
    def commit(self) -> None:
        """Commits any changes made."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rolls backs the changes made."""
        pass

    @classmethod
    def _repo_getter(
        cls,
        model: tp.Type[ModelType],
        repository: tp.Type[RepositoryType],
        name: str,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> tp.Callable[[UnitOfWorkType], RepositoryType]:
        """Gets the function to build the repository instance to use.

        Parameters
        ----------
        model : ModelType
            The :obj:`Model` class to get the repository getter for.
        repository: Type[RepositoryType]
            The repository class to get the repository instance for.
        name : str
            The name of the function to return.
        args : optional
            Additional arguments to pass to the `repository` class's
            constructor.
        kwargs : optional
            Additional keyword-arguments to pass to the `repository`
            class's constructor.

        Returns
        -------
        Callable[[UnitOfWorkBase], RepositoryType]
            A getter function which returns an instantiated instance of
            the given `repository` class.

        """
        def _get_repo(self: UnitOfWorkType) -> RepositoryType:
            return repository(model, self, *args, **kwargs)

        _get_repo.__name__ = name
        _get_repo.__doc__ = (
            f"{repository.__name__}: {model.__name__} storage repository."
        )

        return _get_repo

    @classmethod
    def register(
        cls,
        model: tp.Type[ModelType],
        repository: tp.Type[RepositoryType],
        name: tp.Optional[str] = None,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> None:
        """Registers a storage repository with this unit of work.

        Parameters
        ----------
        model : ModelType
            The model class to register with this unit of work class.
        repository : RepositoryType
            The repository class to use to manage the CRUD operations
            for the given `model`.
        name : str, optional
            The name to register the repository (and access it) with on
            this unit of work.

        Raises
        ------
        ValueError
            If the given `model` is already registered with this class,
            or if the name for the repository is not a valid name.

        """
        if model in cls.__models:
            raise ValueError(f"Model already registered: {model}")
        name = name or camel_to_snake(model.__name__)
        if hasattr(cls, name):
            raise ValueError(f"Class already has attribute: {name}")
        elif not name.isidentifier():
            raise ValueError(f"Invalid attribute name: {name}")

        # - Create and attach property
        get_fn = cls._repo_getter(model, repository, name, *args, **kwargs)
        repo_prop = cached_property(get_fn)
        setattr(cls, name, repo_prop)
        repo_prop.__set_name__(cls, name)

        # - Register ModelType meta
        cls.__models.add(model)
