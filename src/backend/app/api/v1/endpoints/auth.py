# -*- coding: utf-8 -*-
"""
Login API endpoints
"""
from datetime import timedelta
import typing as tp

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm

from app import schema
from app.api import common
from app.core import (
    email,
    security,
)
from app.core.config import settings
from app.crud.base import (
    IUnitOfWork,
    models,
)


router = APIRouter()


@router.post("/login/access-token", response_model=schema.Token)
async def login_access_token(
    *,
    uow: IUnitOfWork = Depends(common.get_uow),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> tp.Dict[str, str]:
    """OAuth2 compatible login to get access token for future requests.
    """
    user = uow.user.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
        )
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.uid,
            expires_delta=expires,
        ),
        "token_type": "bearer",
    }


@router.post("/logout", response_model=schema.Msg)
async def logout(
    *,
    current_user: models.User = Depends(common.get_current_user),
) -> tp.Dict[str, str]:
    """Logs out the currently logged-in user."""
    # Any additional actions here
    return {
        'msg': f'Successfully logged out: {current_user.email}',
    }


@router.post("/login/test-token", response_model=schema.User)
async def test_token(
    *,
    current_user: models.User = Depends(common.get_current_user),
) -> models.User:
    """Test access token for validity."""
    return current_user


@router.post("/password-recovery/{email}", response_model=schema.Msg)
async def recover_password(
    user_email: str,
    *,
    uow: IUnitOfWork = Depends(common.get_uow),
) -> tp.Dict[str, str]:
    """Sends a password recovery email."""
    user = uow.user.get_by_email(user_email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist",
        )
    reset_token = security.generate_password_reset_token(user_email)
    email.send_reset_password_email(
        to=user.email,
        email=user_email,
        token=reset_token,
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schema.Msg)
async def reset_password(
    *,
    token: str = Body(...),
    new_password: str = Body(...),
    uow: IUnitOfWork = Depends(common.get_uow),
) -> tp.Dict[str, str]:
    """Resets the user's password from the reset link."""
    email = security.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = uow.user.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_pw = security.get_password_hash(new_password)
    with uow:
        uow.user.update(user, hashed_password=hashed_pw)
    return {"msg": "Password updated successfully"}
