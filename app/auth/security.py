from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storing in the database."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

# Bypass authentication entirely for now
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Always return a dummy user to bypass token verification
    return {"email": "bypass@example.com"}
