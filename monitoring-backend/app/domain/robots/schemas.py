from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.domain.robots.consts import FAN_SPEED_AUTO, LogDetailType, RobotRunningStateAction, RobotStatus


class LogDetailSchema(BaseModel):
    message: str
    type: LogDetailType
    time: float


class RobotRunningStateSchema(BaseModel):
    action: RobotRunningStateAction


class RobotSchema(BaseModel):
    robot_id: UUID
    status: RobotStatus


class RobotUpdateSchema(BaseModel):
    fan_speed: int | Literal[FAN_SPEED_AUTO]


class RobotStateSchema(BaseModel):
    uuid: UUID
    temperature: float
    power_consumption: float
    status: RobotStatus
    fan_speed: int
    uptime: Optional[int]
    logs: list[LogDetailSchema]

    @field_validator("power_consumption")
    @staticmethod
    def result_check(value):
        return round(value, 2)
