from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_add_calculation():
    import uuid
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"

    user_response = client.post("/users/", json={
        "username": "testuser",
        "email": unique_email,
        "password": "testpass"
    })
    assert user_response.status_code == 200
    user_data = user_response.json()
    user_id = user_data["id"]

    # ✅ Re-add payload here
    payload = {
        "a": 10,
        "b": 5,
        "type": "Add",
        "user_id": user_id
    }

    response = client.post("/calculations/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
