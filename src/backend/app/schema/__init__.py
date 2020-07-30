# -*- coding: utf-8 -*-
"""
Schema for API communications.
"""
from app.schema.message import Msg
from app.schema.name import (
    Name,
    NameCreate,
    NameStored,
    NameUpdate,
)
from app.schema.token import (
    Token,
    TokenPayload,
)
from app.schema.user import (
    User,
    UserCreate,
    UserStored,
    UserUpdate,
)

__all__ = [
    'Msg',
    'Name',
    'NameCreate',
    'NameStored',
    'NameUpdate',
    'Token',
    'TokenPayload',
    'User',
    'UserCreate',
    'UserStored',
    'UserUpdate',
]
