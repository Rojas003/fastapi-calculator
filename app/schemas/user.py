from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

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

class UserPreferences(BaseModel):
    theme: Optional[Literal["light", "dark", "auto"]] = "light"
    language: Optional[Literal["en", "es", "fr"]] = "en"
    timezone: Optional[str] = "UTC"
    notifications_enabled: Optional[bool] = True
    email_notifications: Optional[bool] = True
    calculation_history_limit: Optional[int] = 100
    auto_save_calculations: Optional[bool] = True

class UserPreferencesUpdate(BaseModel):
    theme: Optional[Literal["light", "dark", "auto"]] = None
    language: Optional[Literal["en", "es", "fr"]] = None
    timezone: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    calculation_history_limit: Optional[int] = None
    auto_save_calculations: Optional[bool] = None

class UserProfileResponse(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    
    # NEW: Include preferences in profile response
    theme: str = "light"
    language: str = "en"
    timezone: str = "UTC"
    notifications_enabled: bool = True
    email_notifications: bool = True
    calculation_history_limit: int = 100
    auto_save_calculations: bool = True
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True