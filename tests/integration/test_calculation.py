from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_add_calculation():
    payload = {
        "a": 10,
        "b": 5,
        "type": "Add"
    }
    response = client.post("/calculations/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert "result" in data
    assert data["result"] == 15
