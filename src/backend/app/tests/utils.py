# -*- coding: utf-8 -*-
"""
Unit test utilities.
"""
import random
import string

import requests

from app.core.config import settings


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_server_api():
    server_name = "http://"
    if settings.SERVER_NAME:
        server_name += f"{settings.SERVER_NAME}"
    else:
        server_name += f"{settings.SERVER_HOST}"
        if settings.SERVER_PORT:
            server_name += f":{settings.SERVER_PORT}"
    return server_name + "/api/"


def get_superuser_token_headers():
    server_api = get_server_api()
    login_data = {
        "username": settings.FIRST_ADMIN_USER,
        "password": settings.FIRST_ADMIN_PASSWORD,
    }
    r = requests.post(
        f"{server_api}{settings.API_VERSION}/login/access-token",
        data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
