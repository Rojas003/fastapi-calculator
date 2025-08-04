from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Bypass authentication entirely
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Always return a dummy user to bypass token verification
    return {"email": "bypass@example.com"}
