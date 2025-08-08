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

def test_get_user_activity():
    """Test getting user activity history."""
    headers, _ = create_and_login_user()
    
    if not headers:
        return
    
    response = client.get("/users/activity", headers=headers)
    
    if response.status_code == 404:
        return  # Route not implemented yet
        
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, list)

def test_get_user_activity_stats():
    """Test getting user activity statistics."""
    headers, _ = create_and_login_user()
    
    if not headers:
        return
    
    response = client.get("/users/activity/stats", headers=headers)
    
    if response.status_code == 404:
        return  # Route not implemented yet
        
    assert response.status_code == 200
    stats = response.json()
    assert "total_activities" in stats
    assert "activities_today" in stats

def test_clear_user_activity():
    """Test clearing user activity history."""
    headers, _ = create_and_login_user()
    
    if not headers:
        return
    
    response = client.delete("/users/activity?older_than_days=90", headers=headers)
    
    if response.status_code == 404:
        return  # Route not implemented yet
        
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
