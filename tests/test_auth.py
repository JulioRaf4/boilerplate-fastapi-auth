from fastapi.testclient import TestClient
from auth.main import app

client = TestClient(app)


def test_login():
    response = client.post(
        "/auth/login", data={"username": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


# Add more tests for logout and password recovery
