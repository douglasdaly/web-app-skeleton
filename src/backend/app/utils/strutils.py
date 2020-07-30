# -*- coding: utf-8 -*-
"""
String utilities.
"""
import re


def camel_to_snake(s: str) -> str:
    """Converts the given CamelCase name to snake_case.

    Parameters
    ----------
    s : str
        The text to convert.

    Returns
    -------
    str
        The converted text.

    Notes
    -----
    Originally from:
        https://stackoverflow.com/a/1176023

    """
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def snake_to_lower_camel(s: str) -> str:
    """Converts the given snake_case name to lowerCamelCase.

    Parameters
    ----------
    s : str
        The text to convert.

    Returns
    -------
    str
        The converted text.

    """
    return re.sub(r'\_([a-z0-9])', lambda m: m.group(1).upper(), s)


def snake_to_camel(s: str) -> str:
    """Converts the given snake_case name to CamelCase.

    Parameters
    ----------
    s : str
        The text to convert.

    Returns
    -------
    str
        The converted text.

    """
    s = snake_to_lower_camel(s)
    return re.sub(r'([0-9]*)([a-z])', lambda m: m.group(2).upper(), s, count=1)


def camel_to_snake_fast(s: str) -> str:
    """Converts the given text from CamelCase to snake_case, faster.

    This function is *slightly* faster than the :obj:`camel_to_snake`
    implementation, however that comes at the expense of accuracy.
    Please see the warnings below for more information.

    Parameters
    ----------
    s : str
        The text to convert.

    Returns
    -------
    str
        The converted text.

    Warnings
    --------
    This is faster than the :obj:`camel_to_snake` - however that speed
    gain comes with not catching edge-cases such as multiple uppercase
    letters in a row or non-letter characters.

    Notes
    -----
    Originally from:
        https://stackoverflow.com/a/44969381

    """
    return ''.join('_'+x.lower() if x.isupper() else x for x in s).lstrip('_')


def snake_to_camel_fast(s: str) -> str:
    """Converts the given text from snake_case to CamelCase, faster.

    This function is *slightly* faster than the :obj:`snake_to_camel`
    implementation, however that comes at the expense of accuracy.
    Please see the warnings below for more information.

    Parameters
    ----------
    s : str
        The text to convert.

    Returns
    -------
    str
        The converted text.

    Warnings
    --------
    This is faster than the :obj:`snake_to_camel` - however that speed
    gain comes with not catching edge-cases such as multiple uppercase
    letters in a row or non-letter characters.

    """
    return ''.join(x.capitalize() for x in s.split('_'))
