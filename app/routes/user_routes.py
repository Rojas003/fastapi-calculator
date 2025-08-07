import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse  # <-- Add this import
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse
from app.utils.security import get_password_hash, verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter()
logging.basicConfig(level=logging.INFO)

@router.post("/users/register", response_model=UserResponse)
def register_user(user: UserRegisterRequest, db: Session = Depends(get_db)):
    logging.info(f"Attempting to register user: {user.email}")

    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logging.warning(f"Registration failed, user already exists: {user.email}")
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password and create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logging.info(f"User registered successfully: {new_user.email}")
    return new_user

@router.post("/users/login")
def login_user(user: UserLoginRequest, db: Session = Depends(get_db)):
    logging.info(f"Login attempt for user: {user.email}")

    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        logging.warning(f"Login failed for user: {user.email}")
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    token = create_access_token(db_user.id)
    logging.info(f"Login successful for user: {user.email}")
    return {"access_token": token, "token_type": "bearer"}
