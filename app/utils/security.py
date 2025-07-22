from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db

# === Settings ===
SECRET_KEY = "your-secret-key"  # Replace with a secure key or load from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# === Password hashing context ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === OAuth2 setup for token retrieval ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# === Password utilities ===
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# === Authenticate user by username/email and password ===
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# === Generate JWT access token ===
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === Extract current user from token ===
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
