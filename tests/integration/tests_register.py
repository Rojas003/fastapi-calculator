from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user_success():
    response = client.post("/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "strongpassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "created_at" in data
