# -*- coding: utf-8 -*-
"""
Settings for the CLI tool.
"""
import logging

# Running
DEFAULT_WSGI_SERVER = "uvicorn"
"""str: The name of the default WSGI gateway server to run the API with.
"""

MAX_TRIES = 60 * 5
"""int: Maximum number of attempts to make at starting the server."""

WAIT_SECONDS = 1
"""int: Number of seconds to wait between retry attempts."""

SUPPORTED_WSGI_SERVERS = [
    "uvicorn",
]
"""List[str]: The supported WSGI servers allowed."""
