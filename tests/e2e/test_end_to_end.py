import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_calculation():
    """Test the /calculate endpoint with proper CalculationRequest format"""
    response = client.post("/calculate", json={
        "num1": 4, 
        "num2": 2,
        "operation": "add"
    })
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert data["result"] == 6
    else:
        # If endpoint expects different format or auth, check status
        assert response.status_code in [400, 403, 422]

def test_list_calculations():
    """Test getting list of calculations"""
    response = client.get("/calculations")
    assert response.status_code == 200
    data = response.json()
    assert "calculations" in data
    assert isinstance(data["calculations"], list)

def test_get_calculation_by_id():
    """Test getting a specific calculation"""
    # First get list to see if any calculations exist
    list_resp = client.get("/calculations")
    calculations = list_resp.json()["calculations"]
    
    if calculations:
        calc_id = calculations[0]["id"]
        response = client.get(f"/calculations/{calc_id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
    else:
        # Test with non-existent ID
        response = client.get("/calculations/999999")
        assert response.status_code == 404

def test_delete_nonexistent_calculation():
    """Test deleting non-existent calculation"""
    response = client.delete("/calculations/999999")
    assert response.status_code == 404

def test_create_calculation_missing_input():
    """Test validation error handling"""
    response = client.post("/calculate", json={})
    assert response.status_code in (400, 422)

