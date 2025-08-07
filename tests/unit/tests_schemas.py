import pytest
from app.schemas.user import UserCreate
from pydantic import ValidationError

def test_valid_user_create_schema():
    user = UserCreate(
        email="test@example.com",
        password="secure123"
    )
    assert user.email == "test@example.com"

def test_invalid_email_raises_error():
    with pytest.raises(ValidationError):
        UserCreate(
            email="not-an-email",
            password="123"
        )
