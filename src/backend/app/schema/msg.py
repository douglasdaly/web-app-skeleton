# -*- coding: utf-8 -*-
"""
Message schema.
"""
from enum import auto

from app.schema.base import BaseSchema
from app.utils.enumutils import AutoNameEnum


class StatusType(AutoNameEnum):
    """
    Enumerations for status messages.
    """
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    SUCCESS = auto()
    FAILURE = auto()


class Msg(BaseSchema):
    """
    Schema for a very simply message.
    """
    msg: str


class StatusMsg(Msg):
    """
    Schema for status messages.
    """
    type: StatusType = StatusType.INFO
