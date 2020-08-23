# -*- coding: utf-8 -*-
"""
Users API endpoints.
"""
import typing as tp
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from app import schema
from app.api.common import (
    get_current_active_admin,
    get_current_active_user,
    get_uow,
)
from app.core.config import settings
from app.core.email import send_new_account_email
from app.crud.base import (
    IUnitOfWork,
    models,
)


router = APIRouter()


@router.get("/", response_model=tp.List[schema.User])
async def read_users(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_admin),
) -> tp.List[models.User]:
    """Gets all the users specified."""
    users = uow.user.get_multi(skip=skip, limit=limit)
    return users


@router.post("/", response_model=schema.User)
async def create_user(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    user_in: schema.UserCreate,
    current_user: models.User = Depends(get_current_active_admin),
) -> models.User:
    """Creates a new user."""
    user = uow.user.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )

    with uow:
        user = uow.user.create(obj_in=user_in)

    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            to=user_in.email,
            username=user_in.email,
            password=user_in.password,
        )

    return user


@router.put("/me", response_model=schema.User)
async def update_user_me(
    *,
    name: tp.Union[schema.NameCreate, schema.NameUpdate] = Body(None),
    uow: IUnitOfWork = Depends(get_uow),
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """Updates the current user's information."""
    user_in = schema.UserUpdate()
    if name is not None:
        user_in.name = name

    with uow:
        user = uow.user.update(obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schema.User)
async def read_user_me(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """Gets the current user's information."""
    return current_user


@router.get("/open", response_model=schema.User)
async def create_user_open(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    email: EmailStr = Body(...),
    password: str = Body(...),
    name: tp.Optional[schema.NameCreate] = Body(None),
) -> models.User:
    """Registers a new user (via the open registration)."""
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is not allowed",
        )

    user = uow.user.get_by_email(email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email address already exists",
        )
    user_in = schema.UserCreate(email=email, password=password, name=name)
    with uow:
        user = uow.user.create(obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schema.User)
async def read_user_by_id(
    user_id: UUID,
    *,
    uow: IUnitOfWork = Depends(get_uow),
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """Gets a specific user by their unique ID."""
    user = uow.user.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID doesn't exist",
        )
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="Not enough privileges",
        )
    return user


@router.put("/{user_id}", response_model=schema.User)
async def update_user(
    user_id: UUID,
    *,
    uow: IUnitOfWork = Depends(get_uow),
    user_in: schema.UserUpdate = Body(...),
    current_user: models.User = Depends(get_current_active_admin),
) -> models.User:
    """Updates a user's information."""
    user = uow.user.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID doesn't exist",
        )
    with uow:
        user = uow.user.update(obj=user, obj_in=user_in)
    return user
