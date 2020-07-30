# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.api.v1.endpoints import (
    login,
    users,
)

# Configure the router
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
