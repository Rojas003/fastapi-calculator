from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_end_to_end_crud_calculations():
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

    # Step 2: Login
    login_response = client.post("/token", data={
        "username": unique_email,
        "password": "testpass"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create a calculation
    create_response = client.post("/calculate", json={
        "a": 10,
        "b": 5,
        "type": "Add"
    }, headers=headers)
    assert create_response.status_code == 200
    calc_data = create_response.json()
    calc_id = calc_data["id"]
    assert calc_data["result"] == 15

    # Step 4: Retrieve the calculation
    retrieve_response = client.get(f"/calculations/{calc_id}", headers=headers)
    assert retrieve_response.status_code == 200
    assert retrieve_response.json()["id"] == calc_id

    # Step 5: Update the calculation
    update_response = client.put(f"/calculations/{calc_id}", json={
        "a": 20,
        "b": 5,
        "type": "Subtract"
    }, headers=headers)
    assert update_response.status_code == 200
    updated_calc = update_response.json()
    assert updated_calc["result"] == 15  # 20 - 5

    # Step 6: Delete the calculation
    delete_response = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Calculation deleted successfully"
