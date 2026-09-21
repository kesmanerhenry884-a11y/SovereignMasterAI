from fastapi.testclient import TestClient

from api.routes import app


client = TestClient(app)


def test_location_requires_consent():
    response = client.post("/api/v1/location/position", json={"user_id": "test-user", "latitude": 18.5, "longitude": -72.3})
    assert response.status_code == 403


def test_location_consent_position_and_route():
    assert client.post("/api/v1/location/consent", json={"user_id": "route-user", "granted": True, "purpose": "navigation"}).status_code == 200
    assert client.post("/api/v1/location/position", json={"user_id": "route-user", "latitude": 18.5, "longitude": -72.3}).status_code == 200
    route = client.post("/api/v1/location/route", json={"user_id": "route-user", "destination_latitude": 18.51, "destination_longitude": -72.29})
    assert route.status_code == 200
    assert route.json()["data"]["navigation_ready"] is False
