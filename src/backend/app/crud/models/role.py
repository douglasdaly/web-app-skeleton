# -*- coding: utf-8 -*-
"""
Interface for User storage model.
"""
import typing as tp

from app.crud.models.base import Model, ModelBase

RoleType = tp.TypeVar('RoleType', bound='RoleBase')


class Role(Model, tp.Protocol):
    """
    Interface for User objects.
    """
    name: str
    description: tp.Optional[str]


class RoleBase(ModelBase):
    """
    Base class for user objects.
    """
    name: str
    description: tp.Optional[str]
