# -*- coding: utf-8 -*-
"""
Creates the SQLAlchemy driver components needed for sessions.
"""
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.drivers.sqlalchemy.utils import (
    create_db_uri,
    build_engine,
)

db_uri = create_db_uri(
    settings.DB_ENGINE,
    db_name=settings.DB_NAME,
    driver=settings.DB_DRIVER,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    **settings.DB_CONNECT_EXTRA,
)

engine = build_engine(db_uri, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
