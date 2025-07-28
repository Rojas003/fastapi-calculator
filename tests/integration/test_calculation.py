from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_add_calculation():
    # 1. Register a unique user
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    register_response = client.post("/users/", json={
        "username": "testuser",
        "email": unique_email,
        "password": "testpass"
    })
    assert register_response.status_code == 200

    # 2. Login the user to get JWT token
    login_response = client.post("/token", data={
        "username": unique_email,
        "password": "testpass"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Make the calculation request using JWT for authentication
    calc_response = client.post("/calculate", json={
        "a": 10,
        "b": 5,
        "type": "Add"
    }, headers=headers)
    assert calc_response.status_code == 200

    data = calc_response.json()
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
