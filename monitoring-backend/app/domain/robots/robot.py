from decimal import Decimal
from random import randint, uniform
from typing import Optional
from uuid import uuid4, UUID
from time import time as timestamp

import numpy as np

from app.domain.logging.log_history import LogHistory
from app.domain.robots.consts import RobotStatus, POWER_CONSUMPTION_STATUS_MAP, MAX_POWER_CONSUMPTION


class Robot:
    """Represent a robot with a unique identifier, status, boot time, and activity logs."""

    def __init__(self, uuid: UUID, journal: LogHistory):
        self.uuid: uuid4 = uuid
        self.journal: LogHistory = journal
        self._status: RobotStatus = RobotStatus.IDLE
        self._fan_speed: np.int8 = np.int8(randint(0, 100))
        self.temperature: np.float16 = self._read_current_temperature()
        self.power_consumption: np.float16 = np.float16(round(uniform(*POWER_CONSUMPTION_STATUS_MAP[self.status]), 2))
        self.boot_time: Optional[np.uint32] = np.uint32(timestamp())

    def _read_current_temperature(self) -> np.float16:
        """Read current robot temperature."""

        current_temperature = np.float16(Decimal("10") + Decimal("100") - self._fan_speed)

        if current_temperature > 80:
            self.journal.warning(f"Reaching high temperatures {current_temperature}°C.")

        return current_temperature

    def set_auto_fan_speed(self):
        """Set fan speed based on robot power consumption."""

        if self.status is not RobotStatus.OFFLINE:
            self.fan_speed = int(Decimal(
                self.power_consumption / MAX_POWER_CONSUMPTION
            ) * Decimal(100))
            self.journal.info("Setting fan_speed to auto.")

    @property
    def fan_speed(self) -> np.int8:
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, value: int):
        self._fan_speed = max(0, min(100, value))
        self.temperature = self._read_current_temperature()

    @property
    def status(self) -> RobotStatus:
        return self._status

    @status.setter
    def status(self, value: RobotStatus):
        if self._status == RobotStatus.OFFLINE and value != RobotStatus.OFFLINE:
            self.boot_time = np.uint32(timestamp())
        elif self._status != RobotStatus.OFFLINE and value == RobotStatus.OFFLINE:
            self.boot_time = None

        self._status = value

    @property
    def uptime(self) -> Optional[int]:
        """Calculate robot's uptime."""

        if self.status == RobotStatus.OFFLINE:
            return
        return np.uint32(timestamp() - self.boot_time)

    def turn_on(self):
        """Turn on robot power switch."""
        self.status = RobotStatus.RUNNING

    def turn_off(self):
        """Turn off robot power switch."""
        self.status = RobotStatus.IDLE

    def reset(self):
        """Reset boot_time, status and logs."""
        self.journal.warning("The robot attempts to reset.")

        self.boot_time = np.uint32(timestamp())
        self._status: RobotStatus = RobotStatus.IDLE

        self.journal.clear()
