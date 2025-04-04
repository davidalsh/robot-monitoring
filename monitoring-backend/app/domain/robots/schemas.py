from decimal import Decimal
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel

from app.domain.robots.consts import LogDetailType, RobotRunningStateAction, RobotStatus, FAN_SPEED_AUTO


class LogDetailSchema(BaseModel):
    message: str
    type: LogDetailType
    time: Decimal


class RobotRunningStateSchema(BaseModel):
    action: RobotRunningStateAction


class RobotSchema(BaseModel):
    robot_id: UUID
    status: RobotStatus


class RobotUpdateSchema(BaseModel):
    fan_speed: int | Literal[FAN_SPEED_AUTO]


class RobotStateSchema(BaseModel):
    uuid: UUID
    temperature: Decimal
    power_consumption: Decimal
    status: RobotStatus
    fan_speed: int
    uptime: Optional[int]
    logs: list[LogDetailSchema]
