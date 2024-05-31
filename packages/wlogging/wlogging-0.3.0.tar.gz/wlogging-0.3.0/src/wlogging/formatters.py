"""
"""


#[
from __future__ import annotations

import logging
#]


_RED = "\x1b[31m"
_RED_BACKGROUND = "\x1b[41m"
_GREEN = "\x1b[32m"
_YELLOW = "\x1b[33m"
_BLUE = "\x1b[34m"
_MAGENTA = "\x1b[35m"
_CYAN = "\x1b[36m"
_WHITE = "\x1b[37m"
_RESET = "\x1b[0m"


_LEVEL_COLOR_MAPPING = {
    logging.DEBUG: _YELLOW,
    logging.INFO: _GREEN,
    logging.WARNING: _MAGENTA,
    logging.ERROR: _RED,
    logging.CRITICAL: _RED_BACKGROUND,
}


class ColoredFormatter(logging.Formatter, ):
    def format(self, record, ):
        color = _LEVEL_COLOR_MAPPING.get(record.levelno, _RESET, )
        colored_fmt = color + self._fmt + _RESET
        formatter = logging.Formatter(colored_fmt, )
        return formatter.format(record, )


