# -*- coding: utf-8 -*-
"""
Email-related functionality.
"""
import logging
from pathlib import Path
import typing as tp

import emails
from emails.template import JinjaTemplate

from app.core.config import settings


def send_email(
    to: str,
    subject_template: tp.Optional[tp.Union[str, Path]] = None,
    html_template: tp.Optional[tp.Union[str, Path]] = None,
    environment: tp.Optional[tp.Dict[str, tp.Any]] = None,
    attachments: tp.Optional[tp.Dict[str, Path]] = None,
) -> None:
    """Sends the email specified."""
    assert settings.EMAILS_ENABLED, "Emails are not configured"

    # - Arg handling
    if subject_template is None:
        subject_template = ""
    elif isinstance(subject_template, Path):
        with open(subject_template, 'r') as fin:
            subject_template = fin.read()
    if html_template is None:
        html_template = ""
    elif isinstance(html_template, Path):
        with open(html_template, 'r') as fin:
            html_template = fin.read()
    environment = environment or {}
    if isinstance((attachments := attachments or {}), Path):
        attachments = {attachments.name: attachments}

    # - Construct message
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    for name, file in attachments.items():
        with open(file) as fin:
            message.attach(data=fin, filename=name)

    smtp_opts = {
        "host": settings.SMTP_HOST,
        "port": settings.SMTP_PORT,
    }
    if settings.SMTP_TLS:
        smtp_opts["tls"] = True
    if settings.SMTP_USER:
        smtp_opts["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_opts["password"] = settings.SMTP_PASSWORD

    response = message.send(to=to, render=environment, smtp=smtp_opts)
    logging.info(f"Send email result: {response}")


def send_test_email(to: str) -> None:
    """Sends a test email to the address specified."""
    subject = f"{settings.PROJECT_NAME} - Test email"
    template_path = Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html"
    template_data = {
        "project_name": settings.PROJECT_NAME,
        "email": to,
    }
    return send_email(
        to=to,
        subject_template=subject,
        html_template=template_path,
        environment=template_data,
    )


def send_reset_password_email(to: str, email: str, token: str) -> None:
    """Sends a password reset email."""
    subject = f"{settings.PROJECT_NAME} - Password recovery for {email}"
    template_path = Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html"
    template_data = {
        "project_name": settings.PROJECT_NAME,
        "username": email,
        "email": to,
        "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
        "link": f"{settings.SERVER_HOST}/reset-password?token={token}",
    }
    return send_email(
        to=to,
        subject_template=subject,
        html_template=template_path,
        environment=template_data,
    )


def send_new_account_email(to: str, username: str, password: str) -> None:
    """Sends a new account notification email."""
    subject = f"{settings.PROJECT_NAME} - New account for user {username}"
    template_path = Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html"
    template_data = {
        "project_name": settings.PROJECT_NAME,
        "username": username,
        "password": password,
        "email": to,
        "link": settings.SERVER_HOST,
    }
    return send_email(
        to=to,
        subject_template=subject,
        html_template=template_path,
        environment=template_data,
    )
