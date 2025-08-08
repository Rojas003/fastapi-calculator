import pytest
from app.schemas.user import UserProfileUpdate, UserPasswordChange

def test_user_profile_update_schema():
    """Test UserProfileUpdate schema validation."""
    profile_data = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "phone": "555-1234",
        "bio": "Test bio"
    }
    
    profile = UserProfileUpdate(**profile_data)
    assert profile.username == "testuser"
    assert profile.first_name == "Test"
    assert profile.last_name == "User"
    assert profile.phone == "555-1234"
    assert profile.bio == "Test bio"

def test_user_profile_update_partial():
    """Test UserProfileUpdate with partial data."""
    profile_data = {
        "username": "testuser"
    }
    
    profile = UserProfileUpdate(**profile_data)
    assert profile.username == "testuser"
    assert profile.first_name is None
    assert profile.last_name is None

def test_password_change_schema():
    """Test UserPasswordChange schema validation."""
    password_data = {
        "current_password": "oldpass",
        "new_password": "newpass",
        "confirm_password": "newpass"
    }
    
    password_change = UserPasswordChange(**password_data)
    assert password_change.current_password == "oldpass"
    assert password_change.new_password == "newpass"
    assert password_change.confirm_password == "newpass"

def test_password_change_validation():
    """Test password change validation logic."""
    # Test that we can create the schema
    password_data = {
        "current_password": "oldpass123",
        "new_password": "newpass456",
        "confirm_password": "newpass456"
    }
    
    password_change = UserPasswordChange(**password_data)
    assert len(password_change.current_password) > 0
    assert len(password_change.new_password) > 0
    assert password_change.new_password == password_change.confirm_password