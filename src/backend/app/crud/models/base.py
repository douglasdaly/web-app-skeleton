# -*- coding: utf-8 -*-
"""
Base classes for Models.
"""
import typing as tp
from uuid import UUID

ModelType = tp.TypeVar("ModelType", bound='ModelBase')


class Model(tp.Protocol):
    """
    Interface for base model class.
    """
    uid: tp.Optional[UUID]


class ModelBase(object):
    """
    Model storage ultimate base class.
    """

    def __init__(self, *args: tp.Any, **kwargs: tp.Any) -> None:
        self.uid: tp.Optional[UUID] = kwargs.pop('uid', None)
        return super().__init__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(uid={self.uid!r})"
