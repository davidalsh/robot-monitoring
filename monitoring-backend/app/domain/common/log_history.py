from time import time as timestamp
from typing import Optional
from uuid import UUID

from app.domain.robots.consts import LogDetailType
from app.domain.robots.schemas import LogDetailSchema
from logger import get_logger


class LogHistory:
    """Custom Robot logger."""

    def __init__(self, uuid: UUID):
        self.uuid: UUID = uuid
        self.logger = get_logger()
        self.logs: list[LogDetailSchema] = []
        self.log_prefix = f"<Robot {self.uuid}>"

    def info(self, message: str):
        self._create_log(message)

    def warning(self, message: str):
        self._create_log(message, LogDetailType.WARNING)

    def error(self, message: str):
        self._create_log(message, LogDetailType.ERROR)

    def _create_log(self, message: str, log_level: Optional[LogDetailType] = None):
        if log_level == LogDetailType.WARNING:
            self.logger.warning(f"{self.log_prefix} {message}")
            self.logs.append(LogDetailSchema(type=log_level, message=message, time=timestamp()))
        elif log_level == LogDetailType.ERROR:
            self.logger.error(f"{self.log_prefix} {message}")
            self.logs.append(LogDetailSchema(type=log_level, message=message, time=timestamp()))
        else:
            self.logger.info(message)

    def clear(self):
        self.logs.clear()
