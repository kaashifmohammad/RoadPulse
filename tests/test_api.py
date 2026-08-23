from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "RoadPulse API"


def test_auth_status():
    response = client.get("/api/auth/status")

    assert response.status_code == 200

    data = response.json()

    assert data["authentication"] == "ready"

def test_get_reports():
    response = client.get("/api/reports/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_report_with_ai():
    image_content = b"fake pothole image"

    response = client.post(
        "/api/reports/",
        data={
            "title": "Test Pothole",
            "latitude": "16.3067",
            "longitude": "80.4365",
            "user_id": "1",
        },
        files={
            "image": (
                "pothole.jpg",
                image_content,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Pothole analyzed and report created"
    )

    assert data["complaint_id"] is not None

    assert data["ai"]["pothole_detected"] is True
    assert data["ai"]["severity"] == "HIGH"
    assert data["ai"]["confidence"] == 0.94
    assert data["ai"]["priority"] == "CRITICAL"

    assert data["complaint"]["status"] == "REPORTED"
    assert data["complaint"]["latitude"] == "16.3067"
    assert data["complaint"]["longitude"] == "80.4365"