from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user model for testing
class UserRead(BaseModel):
    id: int
    email: str = "demo@example.com"

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRead:
    # Simulate successful authentication
    return UserRead(id=1)
