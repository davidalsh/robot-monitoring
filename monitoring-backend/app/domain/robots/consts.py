from enum import Enum

FAN_SPEED_AUTO = "auto"


class RobotStatus(str, Enum):
    IDLE = "Idle"
    RUNNING = "Running"
    OFFLINE = "Offline"
    ERROR = "Error"


class RobotRunningStateAction(str, Enum):
    TURN_ON = "on"
    TURN_OFF = "off"


class LogDetailType(str, Enum):
    WARNING = "Warning"
    ERROR = "Error"


POWER_CONSUMPTION_STATUS_MAP = {
    RobotStatus.IDLE: (7, 10),
    RobotStatus.RUNNING: (15, 20),
    RobotStatus.OFFLINE: (0, 0),
    RobotStatus.ERROR: (7, 10),
}
