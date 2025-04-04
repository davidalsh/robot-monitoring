import logging
import os

LOG_LEVEL_MAP = {
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}
custom_log_level = os.environ.get("LOG_LEVEL", "INFO")
if not custom_log_level or custom_log_level not in LOG_LEVEL_MAP:
    raise ValueError("Selected LOG_LEVEL does not exist.")

logger = logging.getLogger("app")
logger.setLevel(LOG_LEVEL_MAP.get(custom_log_level))


def get_logger():
    return logger
