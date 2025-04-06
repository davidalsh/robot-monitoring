import asyncio
from random import random
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_204_NO_CONTENT
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.domain.robots.schemas import RobotRunningStateSchema, RobotSchema, RobotStateSchema, RobotUpdateSchema
from app.domain.robots.services import RobotService
from cli_attr import REFRESH_FREQUENCY_HZ
from logger import get_logger

router = APIRouter(prefix="/api/v1")

logger = get_logger()


@router.get("/robots/")
def list_robots(
    robot_service: RobotService = Depends(RobotService),
) -> list[RobotStateSchema]:
    robots = robot_service.get_all_robots()
    return [RobotStateSchema.from_robot_instance(robot) for robot in robots]


@router.patch("/robots/{robot_id}")
def update_robot(
    robot_id: UUID,
    data: RobotUpdateSchema,
    robot_service: RobotService = Depends(RobotService),
) -> RobotUpdateSchema:
    robot = robot_service.update_robot(robot_id, data)
    return RobotUpdateSchema(fan_speed=robot.fan_speed)


@router.post("/robots/{robot_id}/power")
def toggle_robot_running_state(
    robot_id: UUID,
    status: RobotRunningStateSchema,
    robot_service: RobotService = Depends(RobotService),
) -> RobotSchema:
    robot = robot_service.toggle_robot_status(robot_id, status.action)
    return RobotSchema(robot_id=robot.uuid, status=robot.status)


@router.post("/robots/{robot_id}/reset", status_code=HTTP_204_NO_CONTENT)
def reset_robot(robot_id: UUID, robot_service: RobotService = Depends(RobotService)):
    robot_service.reset_robot(robot_id)


@router.websocket("/ws/robots/state")
async def state_websocket(websocket: WebSocket, robot_service: RobotService = Depends(RobotService)):
    await websocket.accept()
    robots = robot_service.get_all_robots()
    previous_robots = {robot.uuid: RobotStateSchema.from_robot_instance(robot) for robot in robots}

    try:
        while True:
            robots = robot_service.get_all_robots()
            for robot in robots:
                real_temperature = robot.temperature
                robot.temperature += random()  # imitation of temperature change
                current_data = RobotStateSchema.from_robot_instance(robot)
                if current_data != previous_robots.get(robot.uuid):
                    await websocket.send_json(current_data.model_dump(mode="json"))
                    previous_robots[robot.uuid] = current_data
                robot.temperature = real_temperature

            await asyncio.sleep(1 / REFRESH_FREQUENCY_HZ)
    except WebSocketDisconnect:
        logger.info("Websocket disconnect.")
