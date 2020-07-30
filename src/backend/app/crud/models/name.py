# -*- coding: utf-8 -*-
"""
Interface for Name storage model.
"""
import typing as tp

from app.crud.models.base import Model, ModelBase

NameType = tp.TypeVar('NameType', bound='NameBase')


class Name(Model, tp.Protocol):
    """
    Interface for Name objects.
    """
    title: tp.Optional[str]
    first: str
    middle: tp.Optional[str]
    last: str
    suffix: tp.Optional[str]
    preferred: tp.Optional[str]


class NameBase(ModelBase):
    """
    Base class for the Name object.
    """
    title: tp.Optional[str]
    first: str
    middle: tp.Optional[str]
    last: str
    suffix: tp.Optional[str]
    preferred: tp.Optional[str]
