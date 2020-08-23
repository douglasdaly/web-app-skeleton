# -*- coding: utf-8 -*-
"""
CLI tool core components and functionality.
"""
from functools import partial
import logging
import typing as tp

import click
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)
import uvicorn

from app.cli.settings import (
    DEFAULT_WSGI_SERVER,
    MAX_TRIES,
    SUPPORTED_WSGI_SERVERS,
    WAIT_SECONDS,
)
from app.cli.utils import (
    get_numeric_level,
    get_log_function,
)
from app.core.config import settings


# Setup
logger = logging.getLogger(__name__)
if settings.DEBUG:
    log_lvl = logging.DEBUG
else:
    log_lvl = get_numeric_level(settings.LOG_LEVEL)
logger.setLevel(log_lvl)

_get_log_fn = partial(get_log_function, logger)


# CLI
CONTEXT_SETTINGS = {
    'allow_extra_args': True,
    'help_option_names': ['-h', '--help'],
    'ignore_unknown_options': True,
}

@click.group(
    context_settings=CONTEXT_SETTINGS,
    invoke_without_command=True,
)
@click.option('--verbose', is_flag=True, default=False, help="Verbose output")
@click.pass_context
def main(
    ctx: click.Context,
    verbose: bool,
    **kwargs: str,
) -> tp.Optional[int]:
    """
    API Backend CLI Tools
    """
    ctx.ensure_object(dict)
    ctx.obj['is_printing'] = True
    ctx.obj['is_logging'] = False
    ctx.obj['log_level'] = 0
    ctx.obj['verbose'] = verbose

    if ctx.invoked_subcommand is None:
        ctx.forward(run_server)
    return 0


# - Run command

@main.command('run')
@click.argument(
    'server-type',
    nargs=-1,
    type=click.Choice(SUPPORTED_WSGI_SERVERS, case_sensitive=False),
)
@click.option(
    '--host',
    type=click.STRING,
    default=None,
    help="Host to run the API service on.",
)
@click.option(
    '--port',
    type=click.INT,
    default=None,
    help="Port to run the API service on.",
)
@click.option(
    "--log-level",
    type=click.STRING,
    default=None,
    help="Logging level to use for the WSGI server.",
)
@click.pass_context
def run_server(
    ctx: click.Context,
    server_type: tp.Optional[str],
    host: tp.Optional[str],
    port: tp.Optional[int],
    log_level: tp.Optional[str],
    **kwargs: str,
) -> tp.Optional[int]:
    """
    Runs the API through the specified WSGI gateway.
    """
    log = _get_log_fn()

    if not server_type:
        server_type = DEFAULT_WSGI_SERVER
    else:
        server_type = server_type.strip().lower()

    # - Setup
    log(f"Preparing API")
    ctx.obj['log_level'] += 1

    if host is None:
        host = "0.0.0.0" if settings.DEBUG else "127.0.0.1"
    log(f"Host: {host}")

    port = port or settings.SERVER_PORT
    log(f"Port: {port}")

    ctx.obj['log_level'] -= 1

    # - Run
    log(f"Starting {server_type} server")
    ctx.obj['log_level'] += 1
    if server_type == 'uvicorn':
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            log_level=log_level,
            reload=settings.DEBUG,
        )

    ctx.obj['log_level'] -= 1
    return 0


# - Storage commands

@main.group(invoke_without_command=True)
@click.pass_context
def storage(ctx: click.Context, **kwargs: str) -> tp.Optional[int]:
    """
    Storage related CLI tools.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

    return 0


@storage.command('setup')
@click.pass_context
def storage_setup(ctx: click.Context, **kwargs: str) -> tp.Optional[int]:
    """
    Setup the storage system.
    """
    from app.crud.core import setup_storage

    log = _get_log_fn()
    log("Setting up storage system")
    setup_storage()

    return 0


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
)
def _check_storage(log_fn: tp.Callable) -> bool:
    """See if the storage system is alive."""
    from app.crud.core import storage_ready

    try:
        log_fn('Attempting to contact storage system', depth=1)
        result = storage_ready()
        return result
    except Exception as ex:
        log_fn(ex, level=logging.WARN, depth=1)
    return False


@storage.command('check')
@click.pass_context
def storage_check(ctx: click.Context, **kwargs: str) -> tp.Optional[int]:
    """
    Check storage system is ready.
    """
    log = _get_log_fn()
    log("Checking storage system")
    result = _check_storage(log)

    if result:
        log("Storage ready")
    else:
        log("Storage not ready", level=logging.ERROR)
    return 0 if result else 1


# Entry-point
if __name__ == "__main__":
    main(obj={})
