"""Custom logging formatters"""

import logging
from datetime import datetime


class ConsoleFormatter(logging.Formatter):
    """Logging Formatter to add colors to the levelname and include function name"""

    grey = "\x1b[38;21m"
    blue = "\x1b[34m"
    light_blue = "\x1b[94m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    purple = "\x1b[35m"
    reset = "\x1b[0m"

    LEVEL_COLORS = {
        logging.DEBUG: blue,
        logging.INFO: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: purple,
    }

    def __init__(
        self,
        style: str = "%(asctime)s - %(levelname)s - (%(name)s, %(taskName)s) - %(message)s",
        datefmt:str = "%Y-%m-%d %H:%M:%S",
        name:str = "",
    ):
        super().__init__()
        self._style._fmt = style
        self.datefmt = datefmt

    def format(self, record):
        """Format the log record with colors and function name"""

        # Colorize level name
        record.levelname = f"{(
            ConsoleFormatter.LEVEL_COLORS.get(record.levelno, ConsoleFormatter.grey)
            + record.levelname
            + ConsoleFormatter.reset
        ):<17s}"

        return super().format(record)
