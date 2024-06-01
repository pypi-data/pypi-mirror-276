"""Custom logging formatters"""

import logging


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
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        name: str = "",
    ):
        super().__init__()
        self._style._fmt = style
        self.datefmt = datefmt

    def format(self, record):
        """Format the log record with colors and function name"""

        # Determine the color based on the log level
        color_code = ConsoleFormatter.LEVEL_COLORS.get(
            record.levelno, ConsoleFormatter.grey
        )

        # Apply color and reset codes, along with the log level name
        colored_level_name = (
            f"{color_code}{record.levelname}{ConsoleFormatter.reset:<17s}"
        )

        # Replace the original log level name with the colored one
        record.levelname = colored_level_name

        # Format the rest of the log record as usual
        return super().format(record)
