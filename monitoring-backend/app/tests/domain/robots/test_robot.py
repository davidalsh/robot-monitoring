from uuid import uuid4

import pytest

from app.domain.common.log_history import LogHistory
from app.domain.robots.consts import MAX_POWER_CONSUMPTION, RobotStatus
from app.domain.robots.robot import Robot


class TestRobot:
    @pytest.fixture
    def robot(self):
        robot_id = uuid4()
        robot_instance = Robot(robot_id, LogHistory(robot_id))
        return robot_instance

    def test_set_auto_fan_speed_online(self, robot):
        robot.status = RobotStatus.RUNNING
        robot.fan_speed = 0
        robot.set_auto_fan_speed()
        assert robot.fan_speed == int(robot.power_consumption / MAX_POWER_CONSUMPTION * 100)

    def test_set_auto_fan_speed_offline(self, robot):
        robot.status = RobotStatus.OFFLINE
        robot.fan_speed = 0
        robot.set_auto_fan_speed()
        assert robot.fan_speed == 0
