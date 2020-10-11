# -*- coding: utf-8 -*-
"""
Application configuration settings.
"""
import secrets
import typing as tp

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    validator,
)


REQUIRED_ROLES: tp.Dict[str, str] = {
    'admin': 'System administrator role.',
    'user': 'Standard user role.',
}
"""Dict[str, str]: The (minimum) required user roles (and descriptions).
"""


class Settings(BaseSettings):
    """
    API application settings class
    """
    API_VERSION: str = "v1"
    PROJECT_NAME: str = "Backend API"

    # - Environment
    DEBUG: bool = False
    LOG_LEVEL: str = "info"

    # - Server
    SERVER_NAME: str = "backend"
    SERVER_HOST: str
    SERVER_PORT: int = 3000
    SERVER_PROTOCOL: str = "http"

    # - CRUD storage
    CRUD_DRIVER: str = "sqlalchemy"
    CRUD_DRIVERS_EXTRA: tp.Optional[str] = None
    CRUD_DRIVER_MODULE: tp.Optional[str] = None

    # - Security
    BACKEND_CORS_ORIGINS: tp.List[AnyHttpUrl] = []

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    # - Users
    USERS_OPEN_REGISTRATION: bool = False

    FIRST_ADMIN_USER: EmailStr
    FIRST_ADMIN_PASSWORD: str

    # - Database parameters
    DB_ENGINE: str = 'sqlite'
    DB_NAME: tp.Optional[str] = None
    DB_DRIVER: tp.Optional[str] = None
    DB_USER: tp.Optional[str] = None
    DB_PASSWORD: tp.Optional[str] = None
    DB_HOST: tp.Optional[str] = None
    DB_PORT: tp.Optional[int] = None
    DB_CONNECT_EXTRA: tp.Dict[str, tp.Any] = {}

    # - Emails
    EMAILS_ENABLED: bool = False
    EMAILS_FROM_EMAIL: tp.Optional[EmailStr] = None
    EMAILS_FROM_NAME: tp.Optional[str] = None

    EMAIL_TEMPLATES_DIR: str = "./email-templates/"

    SMTP_TLS: bool = True
    SMTP_PORT: tp.Optional[int] = None
    SMTP_HOST: tp.Optional[str] = None
    SMTP_USER: tp.Optional[str] = None
    SMTP_PASSWORD: tp.Optional[str] = None

    # Properties
    @property
    def SERVER_ADDR(self) -> str:
        return (
            f"{self.SERVER_PROTOCOL}://{self.SERVER_HOST}:{self.SERVER_PORT}"
        )

    # Validators
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    @classmethod
    def assemble_cors_origins(
        cls,
        v: tp.Union[str, tp.List[str]],
    ) -> tp.Union[tp.List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("EMAILS_ENABLED", pre=True)
    @classmethod
    def get_emails_enabled(cls, v: bool, values: tp.Dict[str, tp.Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    # Configuration
    class Config:
        case_sensitive: bool = True


settings: Settings = Settings()
"""Settings: The settings in use for the application."""
