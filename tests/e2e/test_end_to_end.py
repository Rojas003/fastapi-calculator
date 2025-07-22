from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_end_to_end_register_login_calculate():
    # Step 1: Register a unique user
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    register_response = client.post("/users/", json={
        "username": "testuser",
        "email": unique_email,
        "password": "testpass"
    })
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Step 2: Log the user in
    login_response = client.post("/token", data={
        "username": unique_email,
        "password": "testpass"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Perform a calculation
    calc_response = client.post("/calculate", json={
        "a": 10,
        "b": 5,
        "type": "Add",
        "user_id": user_id
    }, headers=headers)
    assert calc_response.status_code == 200
    result_data = calc_response.json()
    assert result_data["result"] == 15
