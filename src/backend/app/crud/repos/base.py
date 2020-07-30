# -*- coding: utf-8 -*-
"""
Base components for CRUD-based object storage repositories.
"""
from abc import (
    ABCMeta,
    abstractmethod,
)
import typing as tp
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app.crud.models.base import ModelType
from app.schema.base import (
    CreateSchemaType,
    UpdateSchemaType,
)

RepositoryType = tp.TypeVar("RepositoryType", bound='RepositoryBase')

if tp.TYPE_CHECKING:
    from app.crud.base import UnitOfWorkType


class Repository(tp.Protocol[ModelType]):
    """
    Interface for base repository classes.
    """

    def __init__(
        self,
        model: tp.Type[ModelType],
        uow: 'UnitOfWorkType',
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> None:
        ...

    def get(self, uid: UUID) -> ModelType:
        ...

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: tp.Optional[int] = 100,
    ) -> tp.List[ModelType]:
        ...

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        ...

    def update(
        self,
        obj: ModelType,
        obj_in: tp.Union[tp.Dict[str, tp.Any], CreateSchemaType],
    ) -> ModelType:
        ...

    def remove(self, uid: UUID) -> ModelType:
        ...


class RepositoryBase(
    tp.Generic[ModelType, CreateSchemaType, UpdateSchemaType],
    metaclass=ABCMeta,
):
    """
    Repository base class for CRUD-based object storage.

    Parameters
    ----------
    ModelType : Type[ModelType]
        The ModelType class to manage storage and CRUD operations for.
    uow : UnitOfWorkBase
        The particular unit-of-work instance to use with this
        repository.

    """

    def __init__(
        self,
        model: tp.Type[ModelType],
        uow: 'UnitOfWorkType',
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> None:
        self.model = model
        self.uow = uow

    def _make(self, *args: tp.Any, **kwargs: tp.Any) -> ModelType:
        """Constructs a new object from the given data."""
        return self.model(*args, **kwargs)

    @abstractmethod
    def _save(self, obj: ModelType) -> ModelType:
        """Saves the given `obj` to the underlying storage."""
        pass

    @abstractmethod
    def _load(self, uid: UUID) -> ModelType:
        """Loads the specified object with the given ID."""
        pass

    @abstractmethod
    def _delete(self, obj: ModelType) -> ModelType:
        """Deletes the given object from storage."""
        pass

    # CRUD operations

    def get(self, uid: UUID) -> tp.Optional[ModelType]:
        """Gets the object from the `db` with the given `uid`.

        Parameters
        ----------
        db : Session
            The database session to use to get the object.
        uid : UUID
            The unique ID of the object to get.

        Returns
        -------
        Optional[ModelType]
            The stored object with the given `uid` (if found, ``None``
            otherwise).

        """
        return self._load(uid)

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: tp.Optional[int] = 100,
    ) -> tp.List[ModelType]:
        """Gets multiple objects from the `db` as specified.

        Parameters
        ----------
        db : Session
            The database session to use to get the objects.
        skip : int, optional
            The number of objects to skip (default is ``0``).
        limit : int, optional
            The maximum number of objects to return.  If not specified
            the class's default value will be used (unless a subclass
            overriddes the :obj:`CRUDBase.__default_skip__` attribute,
            the default is ``100``).

        Returns
        -------
        List[ModelType]
            A list of the object(s) requested.

        Raises
        ------
        NotImplementedError
            If this method is not implemented for the particular object
            repository in use.

        """
        raise NotImplementedError()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Creates a new object and stores it.

        Parameters
        ----------
        obj_in : CreateSchemaType
            The data to create the new object using.

        Returns
        -------
        ModelType
            The newly-created and stored object.

        """
        data_in = jsonable_encoder(obj_in, by_alias=False)
        new_obj = self._make(**data_in)
        return self._save(new_obj)

    def update(
        self,
        obj: ModelType,
        obj_in: tp.Union[tp.Dict[str, tp.Any], UpdateSchemaType],
    ) -> ModelType:
        """Updates the existing `obj` using the given `obj_in` data.

        Parameters
        ----------
        obj : ModelType
            The existing object to update.
        obj_in : Union[Dict[str, Any], CreateSchemaType]
            The updated object (or data to update `obj` using) to use.

        Returns
        -------
        ModelType
            The updated object.

        """
        if isinstance(obj_in, dict):
            data_in = obj_in
        else:
            data_in = obj_in.dict(exclude_unset=True)
        upd_obj = self._update(obj, data_in)
        return self._save(upd_obj)

    def _update(
        self,
        obj: ModelType,
        data: tp.Dict[str, tp.Any],
    ) -> ModelType:
        """Updates the given `obj` with the updated `data` given."""
        obj_data = jsonable_encoder(obj, by_alias=False)
        for field in obj_data:
            if field in data:
                setattr(obj, field, data[field])
        return obj

    def remove(self, uid: UUID) -> ModelType:
        """Removes the specified object from storage.

        Parameters
        ----------
        uid : UUID
            The unique ID of the object to remove from storage.

        Returns
        -------
        ModelType
            The removed object.

        Raises
        ------
        ValueError
            If the object with the given `uid` doesn't exist.

        """
        obj = self.get(uid)
        if obj is None:
            raise ValueError(f"No {self.model.__name__} with uid: {uid}")
        return self._delete(obj)
