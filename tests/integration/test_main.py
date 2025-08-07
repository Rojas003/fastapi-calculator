from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_page():
    """Test root page returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_register_page():
    """Test register page returns HTML"""
    response = client.get("/register")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_login_page():
    """Test login page returns HTML"""
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_calculations_page():
    """Test calculations page returns HTML"""
    response = client.get("/calculations-page")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_calculate_page():
    """Test calculate page returns HTML"""
    response = client.get("/calculate")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_add_calculation_page():
    """Test add calculation page returns HTML"""
    response = client.get("/calculations-page/add")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_edit_calculation_page():
    """Test edit calculation page returns HTML"""
    response = client.get("/calculations-page/edit/1")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_add_page():
    """Test add page returns HTML"""
    response = client.get("/add")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_protected_route_no_token():
    """Test protected route without token"""
    response = client.get("/protected")
    assert response.status_code in (401, 403)

def test_protected_route_fake_token():
    """Test protected route with invalid token"""
    headers = {"Authorization": "Bearer faketoken"}
    response = client.get("/protected", headers=headers)
    assert response.status_code in (401, 403)
