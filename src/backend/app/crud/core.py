# -*- coding: utf-8 -*-
"""
Core components for the CRUD subpackage.
"""
from app.drivers.utils import (
    load_driver_function,
    load_repositories_module,
    load_storage_models,
    load_uow_class,
)


# Load essential driver components
models = load_storage_models()
repos = load_repositories_module()

# Load unit-of-work class and setup
UnitOfWork = load_uow_class()

# - Register models with UnitOfWork class
MODEL_MAP = {
    models.Name: repos.NameRepository,
    models.Role: repos.RoleRepository,
    models.User: repos.UserRepository,
}

for m in models.__all__:
    model = getattr(models, m)
    repo = MODEL_MAP.get(model, repos.Repository)
    UnitOfWork.register(model, repo)

# Load required driver functions
create_uow = load_driver_function('create_uow')
init_storage = load_driver_function('init_storage')
setup_storage = load_driver_function('setup_storage')
storage_ready = load_driver_function('storage_ready')
