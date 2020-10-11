# -*- coding: utf-8 -*-
"""
Settings for the CLI tool.
"""
import typing as tp


# Running
DEFAULT_WSGI_SERVER: str = "uvicorn"
"""str: The name of the default WSGI gateway server to run the API with.
"""

MAX_TRIES: int = 60 * 5
"""int: Maximum number of attempts to make at starting the server."""

WAIT_SECONDS: int = 1
"""int: Number of seconds to wait between retry attempts."""

SUPPORTED_WSGI_SERVERS: tp.List[str] = [
    "uvicorn",
]
"""List[str]: The supported WSGI servers allowed."""
