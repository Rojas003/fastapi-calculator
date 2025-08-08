from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserRegisterRequest(UserBase):
    password: str

class UserLoginRequest(UserBase):
    password: str

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None

class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class UserProfileResponse(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
