import logging
import sys


class CustomFormatter(logging.Formatter):
    """CustomFormatter class for styling the logs.
    """

    grey = "\x1b[38;20m"
    green = "\x1b[33;32m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    formatter = "%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s"

    FORMATS = {
        logging.DEBUG: green + formatter + reset,
        logging.INFO: grey + formatter + reset,
        logging.ERROR: red + formatter + reset,
        logging.CRITICAL: bold_red + formatter + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    """Logger class for logging messages.
    """
    __logger = None
    __level = None

    def __init__(
        self,
        logger: str or None = None,
        level: str or None = None
    ) -> None:
        if logger is None:
            return

        self.__logger = logger
        self.__level = level

        log_level = None
        log_stream = None

        if self.__level == "debug":
            log_level = logging.DEBUG
            log_stream = sys.stdout
        else:
            log_level = logging.INFO
            log_stream = sys.stdout

        self.__logger.setLevel(log_level)
        sh = logging.StreamHandler(log_stream)
        sh.setLevel(log_level)
        sh.setFormatter(CustomFormatter())

        if self.__logger.hasHandlers():
            self.__logger.handlers.clear()

        self.__logger.addHandler(sh)

    def info(self, message):
        """Log info function. Logging informational messages.

        Args:
            message (string): Message to be displayed
        """
        self.__logger.info(message)

    def debug(self, message):
        """Log debug function. Logging debug messages.

        Args:
            message (string): Message to be displayed
        """
        self.__logger.debug(message)

    def error(self, message):
        """Log error function. Logging non-fatal errors.

        Args:
            message (string): Message to be displayed
        """
        self.__logger.error(message)

    def critical(self, message):
        """Log critical function. Logging fatal errors and exit the process.

        Args:
            message (string): Message to be displayed
        """
        self.__logger.critical(message)

        sys.exit(1)

    @property
    def level(self) -> str:
        return self.__level

    @property
    def logger(self) -> str:
        return self.__logger
