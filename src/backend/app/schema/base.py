# -*- coding: utf-8 -*-
"""
Base Schema classes for Pydantic serialization.
"""
import typing as tp

import orjson
import pydantic

from app.utils.strutils import snake_to_lower_camel

CreateSchemaType = tp.TypeVar("CreateSchemaType", bound="BaseSchema")
UpdateSchemaType = tp.TypeVar("UpdateSchemaType", bound="BaseSchema")


class BaseSchema(pydantic.BaseModel):
    """
    :obj:`pydantic.BaseModel` extension using orjson encoders.
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class BaseSchemaJS(BaseSchema):
    """
    :obj:`BaseModel` extension using lowerCamelCase aliases for JS.
    """

    class Config:
        alias_generator = snake_to_lower_camel
        allow_population_by_field_name = True
