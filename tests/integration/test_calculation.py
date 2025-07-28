# tests/integration/test_calculation.py

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_add_calculation():
    # Create a unique user
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    password = "testpass"

    # ✅ Register the user
    user_response = client.post("/users/", json={
        "username": "testuser",
        "email": unique_email,
        "password": password
    })
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]

    # ✅ Log in to get the token
    token_response = client.post("/token", data={
        "username": unique_email,
        "password": password
    })
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # ✅ Call the protected /calculate endpoint
    payload = {
        "a": 10,
        "b": 5,
        "type": "Add"
    }

    response = client.post("/calculate", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
    assert data["user_id"] == user_id
