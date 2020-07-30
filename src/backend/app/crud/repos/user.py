# -*- coding: utf-8 -*-
"""
User object storage repository specification.
"""
from abc import (
    ABCMeta,
    abstractmethod,
)
import typing as tp

from app.core.security import (
    get_password_hash,
    verify_password,
)
from app.crud.repos.base import (
    Repository,
    RepositoryBase,
)
from app.crud.models.user import UserType
from app.schema.user import (
    NameCreate,
    NameUpdate,
    UserCreate,
    UserUpdate,
)


class UserRepository(Repository, tp.Protocol):
    """
    Interface for UserRepository objects.
    """

    def get_by_email(self, email: str) -> tp.Optional[UserType]:
        ...

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> tp.Optional[UserType]:
        ...


class UserRepositoryBase(
    RepositoryBase[UserType, UserCreate, UserUpdate],
    metaclass=ABCMeta,
):
    """
    User object storage repository base class.
    """

    @abstractmethod
    def get_by_email(self, email: str) -> tp.Optional[UserType]:
        """Gets the user with the associated `email` given.

        Parameters
        ----------
        email : str
            The user's email address to get the associated User object
            for.

        Returns
        -------
        Optional[ModelType]
            The user with the matching `email` (if found, ``None``
            otherwise).

        """
        pass

    def _make(self, *args: tp.Any, **kwargs: tp.Any) -> UserType:
        kwargs['hashed_password'] = get_password_hash(kwargs.pop('password'))
        name_in = kwargs.pop('name', None)
        if name_in:
            kwargs['name'] = self.uow.name.create(obj_in=NameCreate(**name_in))
        return super()._make(*args, **kwargs)

    def _update(self, obj: UserType, data: tp.Dict[str, tp.Any]) -> UserType:
        if 'password' in data:
            data['hashed_password'] = get_password_hash(data.pop('password'))
        name_in = data.pop('name', None)
        if name_in:
            if obj.name is None:
                name = self.uow.name.create(
                    obj_in=NameCreate(**name_in)
                )
            else:
                name = self.uow.name.update(
                    obj=obj.name,
                    obj_in=NameUpdate(**name_in),
                )
            data['name'] = name
        return super()._update(obj, data)

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> tp.Optional[UserType]:
        """Authenticates (and returns) the user with given credentials.

        Parameters
        ----------
        email : str
            The user's email address.
        password : str
            The plaintext password to validate.

        Returns
        -------
        Optional[ModelType]
            The authenticated User object (if verified, ``None``
            otherwise).

        """
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
