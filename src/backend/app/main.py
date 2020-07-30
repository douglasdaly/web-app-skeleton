# -*- coding: utf-8 -*-
"""
API application entrypoint.
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.utils import get_api_router
from app.core.config import settings


# Create application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json",
)

# Set CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(x) for x in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Router setup
api_router = get_api_router(settings.API_VERSION)
app.include_router(api_router, prefix="/api")
