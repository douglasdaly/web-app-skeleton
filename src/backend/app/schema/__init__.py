# -*- coding: utf-8 -*-
"""
Schema for API communications.
"""
from app.schema.msg import (
    Msg,
    StatusMsg,
)
from app.schema.name import (
    Name,
    NameCreate,
    NameStored,
    NameUpdate,
)
from app.schema.role import (
    Role,
    RoleCreate,
    RoleStored,
    RoleUpdate,
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
    'Role',
    'RoleCreate',
    'RoleStored',
    'RoleUpdate',
    'StatusMsg',
    'Token',
    'TokenPayload',
    'User',
    'UserCreate',
    'UserStored',
    'UserUpdate',
]
