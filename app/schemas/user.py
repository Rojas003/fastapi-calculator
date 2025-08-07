from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Registration request schema
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

# Login request schema
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response schema for returning user info (excluding password)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True