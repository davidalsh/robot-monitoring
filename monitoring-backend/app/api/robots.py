import time
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_204_NO_CONTENT
from starlette.websockets import WebSocket

from app.domain.robots.schemas import RobotStateSchema, RobotSchema, RobotRunningStateSchema, RobotUpdateSchema
from app.domain.robots.services import RobotService

router = APIRouter(prefix="/api/v1")


@router.get("/robots/")
def list_robots(robot_service: RobotService = Depends(RobotService)) -> list[RobotSchema]:
    robots = robot_service.get_all_robots()
    return [RobotSchema(robot_id=robot.uuid, status=robot.status) for robot in robots]


@router.patch("/robots/{robot_id}")
def update_robot(
    robot_id: UUID,
    data: RobotUpdateSchema,
    robot_service: RobotService = Depends(RobotService),
) -> RobotSchema:
    robot = robot_service.update_robot(robot_id, data)
    return RobotSchema(robot_id=robot.uuid, status=robot.status)


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
    robots = robot_service.get_all_robots()
    await websocket.accept()
    previous_robots = {}
    while True:
        for robot in robots:
            current_data = RobotStateSchema(
                uuid=robot.uuid,
                temperature=robot.temperature,
                power_consumption=robot.power_consumption,
                status=robot.status,
                fan_speed=robot.fan_speed,
                uptime=None,
                logs=robot.journal.logs,
            )
            if current_data != previous_robots.get(robot.uuid):
                current_data.uptime = robot.uptime
                await websocket.send_json(current_data)
                current_data.uptime = None
                previous_robots[robot.uuid] = current_data
        time.sleep(0.1)
