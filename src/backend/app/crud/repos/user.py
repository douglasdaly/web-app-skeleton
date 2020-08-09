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
from app.schema.name import (
    NameCreate,
    NameUpdate,
)
from app.schema.user import (
    UserCreate,
    UserUpdate,
)


class UserRepository(Repository, tp.Protocol):
    """
    Interface for UserRepository objects.
    """

    def get_by_email(self, email: str) -> tp.Optional[UserType]:
        ...

    def get_by_role(
        self,
        role: tp.Union[
            str,
            tp.Tuple[str, ...],
            tp.List[tp.Union[str, tp.Tuple[str, ...]]],
        ],
        *,
        skip: int = 0,
        limit: tp.Optional[int] = 100,
    ) -> tp.List[UserType]:
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
        Optional[UserType]
            The user with the matching `email` (if found, ``None``
            otherwise).

        """
        pass

    @classmethod
    def _helper_format_roles(
        cls,
        role: tp.Union[
            str,
            tp.Tuple[str, ...],
            tp.List[tp.Union[str, tp.Tuple[str, ...]]],
        ],
    ) -> tp.List[tp.Tuple[str, ...]]:
        """Helper function for formatting input `role` parameters."""
        roles = []
        if isinstance(role, list):
            for r in role:
                roles.extend(cls._helper_format_roles(r))
        else:
            if isinstance(role, str):
                role = (role,)
            if isinstance(role, tuple):
                role = tuple(x.lower() for x in role)
            roles.append(role)
        return roles

    @abstractmethod
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
    ) -> tp.List[UserType]:
        """Gets the list of users with the role(s) given.

        Parameters
        ----------
        role : Union[str, Tuple[str, ...]], or ``list`` thereof, or
        ``None``
            The name of the role (or ``tuple`` of roles) to get the
            users with.  If a ``tuple`` is used, then only users with
            all of these roles are returned.  If a list is given, the
            same logic applies to the items, but the union of all users
            matching any of the listed items is returned.  If given
            ``None`` it will return users without any associated roles.
        skip : int, optional
            The number of users to skip in the result set (default is
            ``0``).
        limit : int, optional
            The number of users to return in the result set (default is
            ``100``).

        Returns
        -------
        List[UserType]
            The user(s) with the given role(s) and matching criteria, if
            any.

        """
        pass

    def _make(self, *args: tp.Any, **kwargs: tp.Any) -> UserType:
        kwargs['hashed_password'] = get_password_hash(kwargs.pop('password'))

        name_in = kwargs.pop('name', None)
        if name_in:
            kwargs['name'] = self.uow.name.create(obj_in=NameCreate(**name_in))

        roles_in = kwargs.pop('roles', None)
        if roles_in:
            roles_in = [self.uow.role.get_by_name(x) for x in roles_in]
            kwargs['roles'] = roles_in

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

        roles_in = data.pop('roles', None)
        if roles_in:
            roles_in = [self.uow.role.get_by_name(x) for x in roles_in]
            data['roles'] = roles_in

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
