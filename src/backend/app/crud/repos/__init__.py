# -*- coding: utf-8 -*-
# flake8: noqa
"""
Repository subpackage for CRUD storage.
"""
from app.crud.repos.base import (
    Repository,
    RepositoryBase,
)
from app.crud.repos.name import (
    NameRepository,
    NameRepositoryBase,
)
from app.crud.repos.user import (
    UserRepository,
    UserRepositoryBase,
)
