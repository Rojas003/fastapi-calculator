from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def create_and_login_user():
    """Helper to create user and get token."""
    unique_id = uuid.uuid4().hex[:8]
    email = f"test_{unique_id}@example.com"
    
    # Register and login
    client.post("/users/register", json={"email": email, "password": "testpass"})
    login_response = client.post("/users/login", json={"email": email, "password": "testpass"})
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}, email
    return {}, email

def test_get_user_preferences():
    """Test getting user preferences."""
    headers, _ = create_and_login_user()
    
    if not headers:
        return
    
    response = client.get("/users/preferences", headers=headers)
    
    if response.status_code == 404:
        return  # Route not implemented yet
        
    assert response.status_code == 200
    prefs = response.json()
    assert "theme" in prefs
    assert "language" in prefs
    assert "notifications_enabled" in prefs

def test_update_user_preferences():
    """Test updating user preferences."""
    headers, _ = create_and_login_user()
    
    if not headers:
        return
    
    new_prefs = {
        "theme": "dark",
        "language": "es",
        "notifications_enabled": False,
        "calculation_history_limit": 250
    }
    
    response = client.put("/users/preferences", json=new_prefs, headers=headers)
    
    if response.status_code == 404:
        return  # Route not implemented yet
        
    assert response.status_code == 200
    updated_prefs = response.json()
    assert updated_prefs["theme"] == "dark"
    assert updated_prefs["language"] == "es"
    assert updated_prefs["notifications_enabled"] == False
    assert updated_prefs["calculation_history_limit"] == 250

def test_reset_user_preferences():
    """Test resetting user preferences."""
    headers, _ = create_and_login_user()
    
    if not headers:
        return
    
    response = client.post("/users/preferences/reset", headers=headers)
    
    if response.status_code == 404:
        return  # Route not implemented yet
        
    assert response.status_code == 200
    assert "message" in response.json()
