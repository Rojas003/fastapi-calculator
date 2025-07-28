from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.models.user import User
from app.database import get_db
from app.auth.jwt_handler import create_access_token
from app.auth.security import authenticate_user
from app.crud.user import get_user_by_email, create_user_in_db

router = APIRouter()

# ✅ API route: Raw user registration (used in API tests, not frontend)
@router.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user_in_db(db, user)

# ✅ API route: Login and return JWT access token (for programmatic access)
@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Frontend POST /register (used by register.html via fetch)
@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return JSONResponse(
            content={"message": "Email already registered."},
            status_code=400
        )
    create_user_in_db(db, user)
    return JSONResponse(
        content={"message": "Registered successfully"},
        status_code=201
    )

# ✅ Frontend POST /login (used by login.html via fetch)
@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = authenticate_user(db, user.email, user.password)
    if not auth_user:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=401
        )
    access_token = create_access_token(data={"sub": auth_user.email})
    return JSONResponse(
        content={"message": "Login successful", "access_token": access_token},
        status_code=200
    )
