# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    roles,
    users,
)

# Configure the router
api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
