# -*- coding: utf-8 -*-
"""
Core components for the CRUD subpackage.
"""
from app.core.config import (
    REQUIRED_ROLES,
    settings,
)
from app.drivers.utils import (
    load_driver_function,
    load_repositories_module,
    load_storage_models,
    load_uow_class,
)
from app.schema import (
    RoleCreate,
    UserCreate,
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


def setup():
    """Sets up the storage system for initial use."""
    setup_storage()

    uow = create_uow()

    # - Make necessary roles
    for name, desc in REQUIRED_ROLES.items():
        role = uow.role.get_by_name(name)
        if not role:
            new_role = RoleCreate(name=name, description=desc)
            with uow:
                role = uow.role.create(obj_in=new_role)

    # - Make first admin
    user = uow.user.get_by_email(settings.FIRST_ADMIN_USER)
    if not user:
        new_user = UserCreate(
            email=settings.FIRST_ADMIN_USER,
            password=settings.FIRST_ADMIN_PASSWORD,
            is_superuser=True,
            is_admin=True,
            roles=[x for x in REQUIRED_ROLES],
        )
        with uow:
            user = uow.user.create(obj_in=new_user)


def init():
    """Initializes the storage system."""
    init_storage()


def ready() -> bool:
    """Checks if the storage system is ready.

    Returns
    -------
    bool
        Whether or not the configured storage system is ready.

    """
    return storage_ready()
