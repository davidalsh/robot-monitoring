from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from app.domain.robots.services import robots
from main import app


@pytest.fixture
def api_client():
    return TestClient(app)


@pytest.fixture
def robot():
    return list(robots.items())[0][1]


@pytest.fixture
def robot_id(robot):
    return robot.uuid


class TestRobotsAPI:
    def test_update_robot_200(self, api_client, robot_id):
        response = api_client.patch(f"/api/v1/robots/{robot_id}", json={
            "fan_speed": 20,
        })
        assert response.status_code == 200
        assert response.json()["fan_speed"] == 20

    def test_update_robot_auto_200(self, api_client, robot_id, robot):
        current_fan_speed = robot.fan_speed
        response = api_client.patch(f"/api/v1/robots/{robot_id}", json={
            "fan_speed": "auto",
        })
        assert response.status_code == 200
        assert response.json()["fan_speed"] != current_fan_speed

    def test_update_robot_404(self, api_client):
        response = api_client.patch(f"/api/v1/robots/{uuid4()}", json={
            "fan_speed": "auto",
        })
        assert response.status_code == 404

    def test_update_robot_422(self, api_client, robot_id):
        response = api_client.patch(f"/api/v1/robots/WRONG_UUID", json={
            "fan_speed": "auto",
        })
        assert response.status_code == 422

        response = api_client.patch(f"/api/v1/robots/{robot_id}", json={
            "fan_speed": "autsso",
        })
        assert response.status_code == 422

    def test_update_robot_400(self, api_client, robot_id):

        response = api_client.patch(f"/api/v1/robots/{robot_id}", json={
            "fan_speed": 20000,
        })
        assert response.status_code == 400

        response = api_client.patch(f"/api/v1/robots/{robot_id}", json={
            "fan_speed": -10000,
        })
        assert response.status_code == 400
