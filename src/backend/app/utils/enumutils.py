# -*- coding: utf-8 -*-
"""
Enumeration utilities.
"""
from enum import Enum


class AutoNameEnum(Enum):
    """
    Enumeration class for generating enum values (from ``auto()``) using
    the enumeration's variable name.
    """
    def _generate_next_value_(name, start, count, last_values):
        return name
