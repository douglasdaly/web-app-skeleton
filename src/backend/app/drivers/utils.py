# -*- coding: utf-8 -*-
"""
Core functionality for the drivers subpackage.
"""
from types import (
    FunctionType,
    ModuleType,
)
import typing as tp

from app.core.config import settings
from app.crud.base import (
    IModels,
    IRepos,
    UnitOfWorkBase,
)
from app.utils.importutils import (
    load_module,
    load_object,
)


DRIVERS_PACKAGE = "app.drivers"
"""str: Package name for the application's built-in storage drivers."""


def _load_from_driver(
    driver: tp.Optional[str],
    name: tp.Optional[str] = None,
    *,
    raise_ex: bool = True,
    package: tp.Optional[str] = None,
    module: tp.Optional[str] = None,
) -> tp.Any:
    """Helper function to load driver objects.

    Will first attempt to load the driver specified from the
    :obj:`settings.CRUD_DRIVERS_EXTRA` package/location.  If that's not
    defined or if the specified `driver` cannot be found, then it will
    attempt to load it from the built-in :obj:`DRIVERS_PACKAGE`
    location.  Hence, if there two drivers with the same name (one
    built-in and one in the extra location), the extra/non-built-in one
    takes precedence).

    Parameters
    ----------
    driver : str, optional
        The name of the driver package to load from (if ``None``, then
        the :obj:`DRIVERS_PACKAGE` value is used).
    name : str, optional
        The name of the object to load from the


    """
    driver = driver or settings.CRUD_DRIVER
    package = package or DRIVERS_PACKAGE
    module = module or 'core'
    builtin = package == DRIVERS_PACKAGE

    location = f"{package}.{driver}"
    if module:
        location = f"{location}.{module}"

    # - Try to load from extras (if specified)
    if settings.CRUD_DRIVERS_EXTRA and builtin:
        try:
            return _load_from_driver(
                driver,
                name=name,
                raise_ex=True,
                package=settings.CRUD_DRIVERS_EXTRA,
                module=settings.CRUD_DRIVER_MODULE,
            )
        except AttributeError:
            if raise_ex:
                raise
            return None
        except ImportError:
            pass

    # - Try to load from built-in drivers
    if name:
        return load_object(location, name, raise_ex=raise_ex)
    return load_module(location, raise_ex=raise_ex)


def load_driver(
    driver: tp.Optional[str] = None,
    *,
    raise_ex: bool = True,
) -> ModuleType:
    """Loads CRUD storage driver module.

    Parameters
    ----------
    driver : str, optional
        The name of the driver to load the storage schema from (if not
        provided the :obj:`settings.CRUD_DRIVER` is used).
    raise_ex : bool, optional
        Whether or not to raise an exception if an error occurs (default
        is ``True``, raise exceptions).

    Returns
    -------
    ModuleType
        The module containing all the driver object for the given
        `driver`.

    Raises
    ------
    ImportError
        If the driver, with the given `driver` name, can't be imported.

    """
    return _load_from_driver(driver, raise_ex=raise_ex)


def load_uow_class(
    driver: tp.Optional[str] = None,
    *,
    raise_ex: bool = True,
) -> tp.Type[UnitOfWorkBase]:
    """Loads the unit of work class for the `driver` specified.

    Parameters
    ----------
    driver : str, optional
        The name of the driver to load the :obj:`UnitOfWork` class for
        (if not provided the :obj:`settings.CRUD_DRIVER` is used).
    raise_ex : bool, optional
        Whether or not to raise an exception if an error occurs (default
        is ``True``, raise exceptions).

    Returns
    -------
    Type[UnitOfWork]
        The unit of work class to use for the specified `driver`.

    Raises
    ------
    ImportError
        If the driver, with the given `driver` name, can't be imported.
    AttributeError
        If the :obj:`UnitOfWorkBase` implementation, named
        ``UnitOfWork`` doesn't exist in the `driver` module specified.

    """
    return _load_from_driver(driver, 'UnitOfWork', raise_ex=raise_ex)


def load_storage_models(
    driver: tp.Optional[str] = None,
    *,
    raise_ex: bool = True,
) -> IModels:
    """Loads the module containing the object storage models.

    Parameters
    ----------
    driver : str, optional
        The name of the driver to load the storage schema from (if not
        provided the :obj:`settings.CRUD_DRIVER` is used).
    raise_ex : bool, optional
        Whether or not to raise an exception if an error occurs (default
        is ``True``, raise exceptions).

    Returns
    -------
    ModuleType
        The module containing all the storage models for the given
        `driver`.

    Raises
    ------
    ImportError
        If the driver, with the given `driver` name, can't be imported.
    AttributeError
        If the module named ``models`` doesn't exist in the `driver`
        module specified.

    """
    return _load_from_driver(driver, 'models', raise_ex=raise_ex)


def load_repositories_module(
    driver: tp.Optional[str] = None,
    *,
    raise_ex: bool = True,
) -> IRepos:
    """Loads the module containing the CRUD repository classes.

    Parameters
    ----------
    driver : str, optional
        The name of the driver to load the CRUD repository classes from
        (if not provided the :obj:`settings.CRUD_DRIVER` is used).
    raise_ex : bool, optional
        Whether or not to raise an exception if an error occurs (default
        is ``True``, raise exceptions).

    Returns
    -------
    ModuleType
        The module containing all the CRUD storage repository classes
        for the given `driver`.

    Raises
    ------
    ImportError
        If the driver, with the given `driver` name, can't be imported.
    AttributeError
        If the module named ``repos`` doesn't exist in the `driver`
        module specified.

    """
    return _load_from_driver(driver, 'repos', raise_ex=raise_ex)


def load_driver_function(
    name: str,
    driver: tp.Optional[str] = None,
    *,
    raise_ex: bool = True,
) -> FunctionType:
    """Loads the unit-of-work factory function.

    Parameters
    ----------
    name : str
        The name of the function to load from the `driver`.
    driver : str, optional
        The name of the driver to load the function from (if not
        provided the :obj:`settings.CRUD_DRIVER` is used).
    raise_ex : bool, optional
        Whether or not to raise an exception if an error occurs (default
        is ``True``, raise exceptions).

    Returns
    -------
    FunctionType
        The function requested.

    Raises
    ------
    ImportError
        If the driver, with the given `driver` name, can't be imported.
    AttributeError
        If the function with the specified `name` doesn't exist in the
        `driver` module specified.

    """
    return _load_from_driver(driver, name, raise_ex=raise_ex)
