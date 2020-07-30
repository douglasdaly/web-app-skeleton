# -*- coding: utf-8 -*-
"""
Import-related utilities.
"""
import importlib
from types import ModuleType
import typing as tp


def load_module(
    name: str,
    *,
    raise_ex: bool = True
) -> tp.Optional[ModuleType]:
    """Attempts to load the module with the `name` specified.

    Parameters
    ----------
    name : str
        The (full) name of the module to get.

    Returns
    -------
    ModuleType
        The (dynamically-loaded) module with the `name` given.

    Raises
    ------
    ImportError
        If no module is found matching the given `name`.

    """
    try:
        return importlib.import_module(name)
    except ImportError:
        if raise_ex:
            raise
        return None


def load_object(module: str, name: str, *, raise_ex: bool = True) -> tp.Any:
    """Loads the specified object from the specified `module`.

    Parameters
    ----------
    module : str
        The (full) name of the module to load the object from.
    name : str
        The name of the object to load from the given `module`.
    raise_ex : bool, optional
        Whether or not to raise an exception if the  `module` can't be
        found or the attribute with the given `name` on that module
        doesn't exist (default is ``True``, raise exceptions).

    Returns
    -------
    Any
        The (dynamically-loaded) object with the specified `name` from
        the specified `module` (if found).  If `raise_ex` is ``False``
        then ``None`` will be returned if there's an error.

    Raises
    ------
    ImportError
        If no module exists with the specified `module` name and
        `raise_ex` is set to ``True``.
    AttributeError
        If no object with the specified `name` exists on the specified
        `module` and `raise_ex` is set to ``True``.

    """
    try:
        mod = load_module(module, raise_ex=raise_ex)
    except ImportError:
        if raise_ex:
            raise
        return None

    try:
        ret = getattr(mod, name)
    except AttributeError:
        if raise_ex:
            raise
        return None
    return ret
