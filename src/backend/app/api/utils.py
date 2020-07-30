# -*- coding: utf-8 -*-
"""
Core functionality for the API routers.
"""
from fastapi import APIRouter

from app.core.config import settings
from app.utils.importutils import load_object


def get_api_router(version: str) -> APIRouter:
    """Gets the API version's router specified.

    Parameters
    ----------
    version : str
        The version string for the API router to get (e.g. ``"v1"``).

    Returns
    -------
    APIRouter
        The (dynamically-loaded) :obj:`APIRouter` for the requested API
        `version` given.

    Raises
    ------
    ImportError
        If ``DEBUG`` is set to ``True`` in the application's settings
        and no module is found matching the given `version`.
    ValueError
        If ``DEBUG`` is set to ``False`` in the application's settings
        and no module is found matching the given `version`.

    """
    try:
        return load_object(f"app.api.{version}.api", 'api_router')
    except Exception:
        if settings.DEBUG:
            raise
        raise ValueError(f"API version not found: {version}")
