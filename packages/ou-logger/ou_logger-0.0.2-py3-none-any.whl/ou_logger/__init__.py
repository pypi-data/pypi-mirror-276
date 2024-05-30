from .logger import logger, set_handler
import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

__all__ = ["logger", "set_handler", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
