from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def create_user_and_login():
    unique_email = f"neguser_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/users/", json={
        "username": "neguser",
        "email": unique_email,
        "password": "testpass"
    })
    login_response = client.post("/token", data={
        "username": unique_email,
        "password": "testpass"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_calculation_unauthorized():
    # No token provided
    response = client.post("/calculate", json={"a": 10, "b": 5, "type": "Add"})
    assert response.status_code == 401

def test_calculation_invalid_input():
    headers = create_user_and_login()

    # Invalid operation type
    response = client.post("/calculate", json={
        "a": 10,
        "b": 5,
        "type": "InvalidOp"
    }, headers=headers)
    assert response.status_code == 400

    # Division by zero
    response = client.post("/calculate", json={
        "a": 10,
        "b": 0,
        "type": "Divide"
    }, headers=headers)
    assert response.status_code in [400, 422]

def test_calculation_non_existent_update_delete():
    headers = create_user_and_login()

    # Update non-existent calculation
    update_response = client.put("/calculations/999999", json={
        "a": 10,
        "b": 5,
        "type": "Add"
    }, headers=headers)
    assert update_response.status_code == 404

    # Delete non-existent calculation
    delete_response = client.delete("/calculations/999999", headers=headers)
    assert delete_response.status_code == 404
