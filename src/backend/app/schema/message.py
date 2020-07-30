# -*- coding: utf-8 -*-
"""
Message schema.
"""
from app.schema.base import BaseSchema


class Msg(BaseSchema):
    """
    Schema for a very simply message.
    """
    msg: str
