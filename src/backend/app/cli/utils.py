# -*- coding: utf-8 -*-
"""
Utilities for the CLI tools.
"""
from collections import defaultdict
import logging
import traceback
import typing as tp

import click


_LEVEL_STYLES: tp.Dict[int, tp.Dict[str, tp.Any]] = {
    logging.DEBUG: dict(fg='cyan'),
    logging.INFO: dict(bold=True),
    logging.WARN: dict(fg='yellow', bold=True),
    logging.ERROR: dict(fg='red', bold=True),
}
_DEPTH_STYLES: tp.Dict[int, tp.Dict[str, tp.Any]] = defaultdict(
    lambda: dict(dim=True)
)
_DEPTH_STYLES[0] = {}


class LogCallable(tp.Protocol):
    def __call__(
        self,
        msg: tp.Union[str, Exception],
        level: int = logging.INFO,
        depth: int = 0,
        depth_spacer: str = '-',
        level_style: tp.Optional[tp.Dict[str, tp.Any]] = None,
        depth_style: tp.Optional[tp.Dict[str, tp.Any]] = None,
    ) -> None:
        ...


def get_numeric_level(level: str) -> int:
    """Converts the given log level name to the appropriate number.

    Parameters
    ----------
    level : str
        The name of the logging level to get the associated ``int`` for
        (case-insensitive).

    Returns
    -------
    int
        The ``logging`` module's log level (``int``) associated with the
        given `level`.

    Raises
    ------
    ValueError
        If the given `level` is not a valid logging level.

    """
    try:
        return getattr(logging, level.upper())
    except AttributeError:
        raise ValueError(f"No such logging level: {level.upper()}")


def get_log_function(
    logger: logging.Logger,
    component: tp.Optional[str] = None,
    initial_depth: tp.Optional[int] = None,
    print_out: tp.Optional[bool] = None,
    log_out: tp.Optional[bool] = None,
    verbose: tp.Optional[bool] = None,
) -> LogCallable:
    """Gets a helper log function for component logging."""
    ctx = click.get_current_context()
    if not component:
        component = ctx.info_name.upper() if ctx.info_name else 'SYS'
    else:
        component = component.upper()
    if initial_depth is None:
        initial_depth = ctx.obj.get("log_level", 0)
    if print_out is None:
        print_out = ctx.obj.get("is_printing", True)
    if log_out is None:
        log_out = ctx.obj.get("is_logging", False)
    if verbose is None:
        verbose = ctx.obj.get("verbose", False)

    def _log_fn(
        msg: tp.Union[str, Exception],
        level: int = logging.INFO,
        depth: int = 0,
        depth_spacer: str = '-',
        level_style: tp.Optional[tp.Dict[str, tp.Any]] = None,
        depth_style: tp.Optional[tp.Dict[str, tp.Any]] = None,
    ) -> None:
        cur_depth: int = click.get_current_context().obj.get('log_level', 0)

        depth = (initial_depth or 0) + cur_depth + depth
        spacer = f" {depth_spacer * depth}{' ' if depth > 0 else ''}"

        if level_style is None:
            level_style = _LEVEL_STYLES.get(level, {})
        if depth_style is None:
            depth_style = _DEPTH_STYLES[depth]

        msg_pre = click.style(f"[{component:^5}]", **level_style)
        msg_post = click.style(f"{spacer}{msg!s}", **depth_style)
        full_msg = msg_pre + msg_post

        if print_out:
            click.echo(full_msg)
        if log_out:
            logger.log(level, click.unstyle(full_msg))
        if verbose and isinstance(msg, Exception):
            full_err = traceback.format_exc()
            if print_out:
                click.echo(full_err)
            if log_out:
                logger.log(level, full_err)
        return

    return _log_fn
