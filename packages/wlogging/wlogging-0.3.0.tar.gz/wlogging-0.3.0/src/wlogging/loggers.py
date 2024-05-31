"""
"""


#[
from __future__ import annotations

from types import (MethodType, )
import functools as _ft

import logging
from . import formatters as _formatters
#]


__all__ = (
    "get_colored_logger",
    "get_short_logger",
    "get_colored_two_liner",
)


def get_colored_logger(
    name: str | None = None,
    level: int = logging.WARNING,
    format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    propagate: bool = True,
    remove_existing_handlers: bool = True,
) -> logging.Logger:
    """
    """
    logger = logging.getLogger(name, )
    logger.clear_handlers = MethodType(_clear_handlers, logger, )
    logger.propagate = propagate
    if remove_existing_handlers:
        logger.clear_handlers()
    handler = logging.StreamHandler()
    formatter = _formatters.ColoredFormatter(format, )
    handler.set_formatter(formatter, )
    logger.addHandler(handler, )
    logger.setLevel(level, )
    logger._decorated = True
    return logger


get_short_logger = _ft.partial(
    get_colored_logger,
    format="%(name)s | %(message)s",
)


get_colored_two_liner = _ft.partial(
    get_colored_logger,
    format="%(asctime)s | %(levelname)s | %(name)s:\n::: %(message)s",
)


def _clear_handlers(logger: Logger, ) -> None:
    for handler in logger.handlers:
        logger.remove_handler(handler, )


