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


def test_assign_contractor():
    # Create a report first.
    image_content = b"fake pothole image"

    create_response = client.post(
        "/api/reports/",
        data={
            "title": "Contractor Assignment Test",
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

    assert create_response.status_code == 200

    report_id = create_response.json()["complaint_id"]

    response = client.patch(
        f"/api/reports/{report_id}/contractor",
        json={
            "contractor": "ABC Road Works",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Contractor assigned successfully"
    )

    assert data["report"]["id"] == report_id
    assert data["report"]["contractor"] == (
        "ABC Road Works"
    )
    assert data["report"]["status"] == "ASSIGNED"


def test_update_report_status():
    image_content = b"fake pothole image"

    create_response = client.post(
        "/api/reports/",
        data={
            "title": "Status Workflow Test",
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

    assert create_response.status_code == 200

    report_id = create_response.json()["complaint_id"]

    statuses = [
        "ASSIGNED",
        "IN_PROGRESS",
        "REPAIRED",
        "COMPLETED",
    ]

    for status in statuses:
        response = client.patch(
            f"/api/reports/{report_id}/status",
            json={
                "status": status,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["report"]["id"] == report_id
        assert data["report"]["status"] == status


def test_invalid_report_id_for_contractor():
    response = client.patch(
        "/api/reports/999999/contractor",
        json={
            "contractor": "ABC Road Works",
        },
    )

    assert response.status_code == 404


def test_invalid_report_id_for_status():
    response = client.patch(
        "/api/reports/999999/status",
        json={
            "status": "COMPLETED",
        },
    )

    assert response.status_code == 404


def test_invalid_report_status():
    image_content = b"fake pothole image"

    create_response = client.post(
        "/api/reports/",
        data={
            "title": "Invalid Status Test",
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

    assert create_response.status_code == 200

    report_id = create_response.json()["complaint_id"]

    response = client.patch(
        f"/api/reports/{report_id}/status",
        json={
            "status": "INVALID_STATUS",
        },
    )

    assert response.status_code == 400


def test_empty_contractor():
    image_content = b"fake pothole image"

    create_response = client.post(
        "/api/reports/",
        data={
            "title": "Empty Contractor Test",
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

    assert create_response.status_code == 200

    report_id = create_response.json()["complaint_id"]

    response = client.patch(
        f"/api/reports/{report_id}/contractor",
        json={
            "contractor": "   ",
        },
    )

    assert response.status_code == 400