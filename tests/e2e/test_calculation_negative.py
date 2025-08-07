from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def create_user_and_login():
    """Create user and return auth headers"""
    unique_id = uuid.uuid4().hex[:8]
    unique_email = f"test_{unique_id}@example.com"

    # Register the user
    client.post("/users/register", json={
        "email": unique_email,
        "password": "testpass123"
    })

    # Login the user
    login_response = client.post("/users/login", json={
        "email": unique_email,
        "password": "testpass123"
    })

    token_data = login_response.json()
    if "access_token" not in token_data:
        raise RuntimeError(f"Login failed: {token_data}")

    return {"Authorization": f"Bearer {token_data['access_token']}"}

def test_calculation_unauthorized():
    """Test calculation endpoint without authentication"""
    response = client.post("/calculations", json={
        "operation": "add",
        "num1": 10,
        "num2": 5
    })

    # Your app returns 403, not 401
    assert response.status_code == 403

def test_calculation_invalid_input():
    """Test calculation with invalid inputs"""
    headers = create_user_and_login()

    # Invalid operation type
    response = client.post("/calculations", json={
        "operation": "invalid_operation",
        "num1": 10,
        "num2": 5
    }, headers=headers)
    assert response.status_code == 400

    # Division by zero
    response = client.post("/calculations", json={
        "operation": "divide",
        "num1": 10,
        "num2": 0
    }, headers=headers)
    assert response.status_code == 400

def test_calculation_non_existent_update_delete():
    """Test updating and deleting non-existent calculations"""
    headers = create_user_and_login()

    # Update non-existent calculation
    update_response = client.put("/calculations/999999", json={
        "num1": 10,
        "num2": 5,
        "operation": "add"
    }, headers=headers)
    assert update_response.status_code == 404

    # Delete non-existent calculation
    delete_response = client.delete("/calculations/999999", headers=headers)
    assert delete_response.status_code == 404