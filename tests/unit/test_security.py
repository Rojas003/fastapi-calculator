import pytest
from app.utils.security import get_password_hash, verify_password

def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # Hash should be different from original password
    assert hashed != password
    
    # Should verify correctly
    assert verify_password(password, hashed) == True
    
    # Should not verify with wrong password
    assert verify_password("wrongpassword", hashed) == False

def test_empty_password():
    """Test edge case with empty password"""
    password = ""
    hashed = get_password_hash(password)
    assert verify_password("", hashed) == True
    assert verify_password("notempty", hashed) == False