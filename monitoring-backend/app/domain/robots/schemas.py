from typing import TYPE_CHECKING, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.domain.robots.consts import FAN_SPEED_AUTO, LogDetailType, RobotRunningStateAction, RobotStatus

if TYPE_CHECKING:
    from app.domain.robots.robot import Robot


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
    name: str
    temperature: float
    power_consumption: float
    status: RobotStatus
    fan_speed: int
    boot_time: Optional[int]
    logs: list[LogDetailSchema]

    @field_validator("power_consumption")
    @staticmethod
    def prepare_power_consumption(value: float) -> float:
        return round(value, 2)

    @field_validator("temperature")
    @staticmethod
    def prepare_temperature(value: float) -> float:
        return round(value, 2)

    @staticmethod
    def from_robot_instance(robot: "Robot") -> "RobotStateSchema":
        return RobotStateSchema(
            uuid=robot.uuid,
            name=robot.name,
            temperature=robot.temperature,
            power_consumption=robot.power_consumption,
            status=robot.status,
            fan_speed=robot.fan_speed,
            boot_time=robot.boot_time,
            logs=robot.journal.logs[::-1],
        )
