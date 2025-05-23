from random import randint, uniform
from time import time as timestamp
from typing import Optional
from uuid import UUID, uuid4

import numpy as np

from app.domain.common.log_history import LogHistory
from app.domain.robots.consts import POWER_CONSUMPTION_STATUS_MAP, RobotStatus


class Robot:
    """Represent a robot with a unique identifier, status, boot time, and activity logs."""

    def __init__(self, uuid: UUID, journal: LogHistory):
        self.uuid: uuid4 = uuid
        self.name: str = f"Robot {str(uuid)[:4]}"
        self.journal: LogHistory = journal
        self._status: RobotStatus = RobotStatus.IDLE
        self._fan_speed: np.int8 = np.int8(randint(0, 100))
        self.power_consumption: np.float16 = self._read_power_consumption_sensor()
        self.temperature: np.float16 = self._read_temperature_sensor()
        self.boot_time: Optional[np.uint32] = np.uint32(timestamp())

    def _read_power_consumption_sensor(self) -> np.float16:
        """Read robot current power consumption."""
        return np.float16(uniform(*POWER_CONSUMPTION_STATUS_MAP[self.status]))

    def set_auto_fan_speed(self):
        """Set fan speed based on robot power consumption."""
        if self.status is not RobotStatus.OFFLINE:
            self.fan_speed = int(self.power_consumption / POWER_CONSUMPTION_STATUS_MAP[self.status][1] * 100)
            self.journal.info("Setting fan_speed to auto.")

    def _read_temperature_sensor(self) -> np.float16:
        """Read robot current temperature based on power consumption and fan speed."""
        current_temperature = np.float16(self.power_consumption * 5 * (100 - self.fan_speed) / 100)
        if current_temperature > 80:
            self.journal.error(f"Reached critical temperature {current_temperature}°C.")
            self.status = RobotStatus.ERROR
        elif current_temperature > 60:
            self.journal.warning(f"Reaching high temperatures {current_temperature}°C.")
        return current_temperature

    @property
    def fan_speed(self) -> np.int8:
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, value: int):
        self._fan_speed = max(0, min(100, value))
        self.temperature = self._read_temperature_sensor()

    @property
    def status(self) -> RobotStatus:
        return self._status

    @status.setter
    def status(self, value: RobotStatus):
        """Change robot status, update power consumption basing on new status and set fan speed to auto."""
        if self._status == RobotStatus.OFFLINE and value != RobotStatus.OFFLINE:
            self.boot_time = np.uint32(timestamp())
        elif self._status != RobotStatus.OFFLINE and value == RobotStatus.OFFLINE:
            self.boot_time = None

        self._status = value
        self.power_consumption = self._read_power_consumption_sensor()
        if value != RobotStatus.ERROR:
            self.set_auto_fan_speed()

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
        self.status = RobotStatus.IDLE

        self.journal.clear()
