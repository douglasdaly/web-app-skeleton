# -*- coding: utf-8 -*-
"""
Roles API endpoints.
"""
import typing as tp
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Query,
)
from fastapi.encoders import jsonable_encoder

from app import schema
from app.api.common import (
    get_current_active_admin,
    get_current_active_user,
    get_uow,
)
from app.core.config import settings
from app.crud.base import (
    IUnitOfWork,
    models,
)


router = APIRouter()


@router.get("/{role_id}")
async def read_role_by_id(
    role_id: UUID,
    *,
    uow: IUnitOfWork = Depends(get_uow),
    current_user: models.User = Depends(get_current_active_admin),
) -> models.Role:
    """Gets a specific role by their unique ID."""
    role = uow.role.get(role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role with this ID doesn't exist",
        )
    return role


@router.get("/", response_model=tp.List[schema.Role])
async def read_roles(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    skip: int = Query(0),
    limit: tp.Optional[int] = Query(None),
    current_user: models.User = Depends(get_current_active_admin),
) -> tp.List[models.Role]:
    """Gets all the roles specified."""
    roles = uow.role.get_multi(skip=skip, limit=limit)
    return roles


@router.post("/", response_model=schema.Role)
async def create_role(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    role_in: schema.RoleCreate = Body(...),
    current_user: models.User = Depends(get_current_active_admin),
) -> models.Role:
    """Creates a new role."""
    with uow:
        role = uow.role.create(obj_in=role_in)
    return role


@router.put("/{role_id}", response_model=schema.Role)
async def update_role(
    role_id: UUID,
    *,
    uow: IUnitOfWork = Depends(get_uow),
    role_in: schema.RoleUpdate = Body(...),
    current_user: models.User = Depends(get_current_active_admin),
) -> models.Role:
    """Updates a role's information."""
    role = uow.role.get(role_id)
    if not role:
        raise HTTPException(
            status_code=404,
            detail="The role with this ID doesn't exist",
        )
    with uow:
        role = uow.role.update(obj=role, obj_in=role_in)
    return role
