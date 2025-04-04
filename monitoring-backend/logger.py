import logging

from cli_attr import LOG_LEVEL

LOG_LEVEL_MAP = {
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

logger = logging.getLogger("app")
logger.setLevel(LOG_LEVEL_MAP[LOG_LEVEL])


def get_logger():
    return logger
