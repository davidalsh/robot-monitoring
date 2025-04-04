from typing import Iterable
from uuid import UUID, uuid4

from app.domain.common.exceptions import DetailNotFound, ImpossibleAction
from app.domain.logging.log_history import LogHistory
from app.domain.robots.consts import FAN_SPEED_AUTO, RobotRunningStateAction, RobotStatus
from app.domain.robots.robot import Robot
from app.domain.robots.schemas import RobotUpdateSchema

robots = {robot_id: Robot(robot_id, LogHistory(robot_id)) for robot_id in [uuid4() for _ in range(3)]}


class RobotService:
    @staticmethod
    def get_all_robots() -> Iterable[Robot]:
        """Return all visible robots."""

        return robots.values()

    @staticmethod
    def get_robot_by_id(robot_id: UUID) -> Robot:
        """Return robot using its id."""

        robot = robots.get(robot_id)
        if not robot:
            raise DetailNotFound
        return robot

    def update_robot(self, robot_id: UUID, data: RobotUpdateSchema) -> Robot:
        """Update robot fan speed."""

        robot = self.get_robot_by_id(robot_id)
        if data.fan_speed == FAN_SPEED_AUTO:
            robot.set_auto_fan_speed()
            return robot

        if not (0 <= data.fan_speed <= 100):
            raise ImpossibleAction(message="Robot fan speed must be between 0 and 100.")
        robot.fan_speed = data.fan_speed
        return robot

    def toggle_robot_status(self, robot_id: UUID, action: RobotRunningStateAction) -> Robot:
        """Switch robot power button."""

        robot = self.get_robot_by_id(robot_id)
        if action == RobotRunningStateAction.TURN_ON:
            robot.turn_on()
        else:
            robot.turn_off()

        return robot

    def reset_robot(self, robot_id: UUID):
        """Reset robot logs, boot_time, status if status is error."""

        robot = self.get_robot_by_id(robot_id)
        if robot.status not in [RobotStatus.ERROR, RobotStatus.IDLE]:
            raise ImpossibleAction
        robot.reset()
