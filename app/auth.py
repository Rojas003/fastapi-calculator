from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from app.auth.jwt_bearer import JWTBearer
from app.core.config import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_email
from app.database import get_db
from sqlalchemy.orm import Session

# User schema to return after authentication
class UserRead(BaseModel):
    id: int
    email: str

# Dependency to get current user from token
def get_current_user(
    token: str = Depends(JWTBearer()), 
    db: Session = Depends(get_db)
) -> UserRead:
    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Retrieve user from DB
        user = get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return UserRead(id=user.id, email=user.email)  # ✅ return correct schema
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
