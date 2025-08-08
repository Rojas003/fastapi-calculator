import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse  # <-- Add this import
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse, UserProfileUpdate, UserPasswordChange, UserProfileResponse, UserPreferences, UserPreferencesUpdate
from app.utils.security import get_password_hash, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user

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

@router.get("/users/profile", response_model=UserProfileResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile information."""
    return current_user

@router.put("/users/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile information."""
    logging.info(f"Updating profile for user: {current_user.email}")
    
    # Update only provided fields
    update_data = profile_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = func.now()
    db.commit()
    db.refresh(current_user)
    
    logging.info(f"Profile updated successfully for user: {current_user.email}")
    return current_user

@router.put("/users/change-password")
def change_password(
    password_data: UserPasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password."""
    logging.info(f"Password change attempt for user: {current_user.email}")
    
    # Validate current password
    if not verify_password(password_data.current_password, current_user.password):
        logging.warning(f"Invalid current password for user: {current_user.email}")
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Validate new password confirmation
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    # Validate new password is different
    if verify_password(password_data.new_password, current_user.password):
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    
    # Update password
    current_user.password = get_password_hash(password_data.new_password)
    current_user.updated_at = func.now()
    db.commit()
    
    logging.info(f"Password changed successfully for user: {current_user.email}")
    return {"message": "Password changed successfully"}

@router.get("/users/preferences", response_model=UserPreferences)
def get_user_preferences(current_user: User = Depends(get_current_user)):
    """Get current user's preferences."""
    logging.info(f"Getting preferences for user: {current_user.email}")
    
    return UserPreferences(
        theme=current_user.theme,
        language=current_user.language, 
        timezone=current_user.timezone,
        notifications_enabled=current_user.notifications_enabled,
        email_notifications=current_user.email_notifications,
        calculation_history_limit=current_user.calculation_history_limit,
        auto_save_calculations=current_user.auto_save_calculations
    )

@router.put("/users/preferences", response_model=UserPreferences)
def update_user_preferences(
    preferences: UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user preferences."""
    logging.info(f"Updating preferences for user: {current_user.email}")
    
    # Update only provided fields
    update_data = preferences.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    current_user.updated_at = func.now()
    db.commit()
    db.refresh(current_user)
    
    logging.info(f"Preferences updated successfully for user: {current_user.email}")
    
    return UserPreferences(
        theme=current_user.theme,
        language=current_user.language,
        timezone=current_user.timezone,
        notifications_enabled=current_user.notifications_enabled,
        email_notifications=current_user.email_notifications,
        calculation_history_limit=current_user.calculation_history_limit,
        auto_save_calculations=current_user.auto_save_calculations
    )

@router.post("/users/preferences/reset")
def reset_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reset user preferences to defaults."""
    logging.info(f"Resetting preferences for user: {current_user.email}")
    
    # Reset to defaults
    current_user.theme = "light"
    current_user.language = "en"
    current_user.timezone = "UTC"
    current_user.notifications_enabled = True
    current_user.email_notifications = True
    current_user.calculation_history_limit = 100
    current_user.auto_save_calculations = True
    current_user.updated_at = func.now()
    
    db.commit()
    db.refresh(current_user)
    
    logging.info(f"Preferences reset successfully for user: {current_user.email}")
    return {"message": "Preferences reset to defaults"}
