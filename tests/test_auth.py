from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_login_returns_token_for_valid_teacher():
    response = client.post(
        "/auth/login",
        json={"username": "teacher", "password": "password"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_signup_requires_teacher_authentication():
    response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )

    assert response.status_code == 401


def test_signed_in_teacher_can_register_student():
    login_response = client.post(
        "/auth/login",
        json={"username": "teacher", "password": "password"},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
