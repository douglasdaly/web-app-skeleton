# -*- coding: utf-8 -*-
"""
Token schema.
"""
from uuid import UUID

from app.schema.base import (
    BaseSchema,
    BaseSchemaJS,
)


class Token(BaseSchemaJS):
    """
    Basic access-token schema.
    """
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    """
    Token payload data.
    """
    sub: UUID
