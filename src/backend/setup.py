#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file for application installation.
"""
from setuptools import setup


#
#   Configuration
#

PACKAGES = [
    'app',
]

PYTHON_REQUIRES = ">=3.8"

REQUIRES = [
    "email-validator",
    "emails",
    "fastapi",
    "orjson",
    "passlib[bcrypt]",
    "pydantic",
    "python-jose[cryptography]",
    "python-multipart",
    "sqlalchemy",
    "tenacity",
]

EXTRAS_REQUIRE = {}

ENTRY_POINTS = {}


#
#   Setup
#

setup(
    name='app',
    packages=PACKAGES,
    python_requires=PYTHON_REQUIRES,
    install_requires=REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
)
