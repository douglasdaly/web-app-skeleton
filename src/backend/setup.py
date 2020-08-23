#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file for application installation.
"""
from setuptools import (
    find_packages,
    setup,
)


#
#   Configuration
#

PACKAGES = [
    'app',
    'app.*',
]

PYTHON_REQUIRES = ">=3.8"

REQUIRES = [
    "click",
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
    "uvicorn",
]

EXTRAS_REQUIRE = {
    "postgres": ["psycopg2-binary"],
}

ENTRY_POINTS = {
    "console_scripts": [
        "app=app.cli.core:main",
    ]
}


#
#   Setup
#

setup(
    name='app',
    packages=find_packages(include=PACKAGES),
    python_requires=PYTHON_REQUIRES,
    install_requires=REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
)
