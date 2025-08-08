from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    # PROFILE FIELDS (from previous feature)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    
    # NEW: USER PREFERENCES FIELDS 🎨
    theme = Column(String, default="light")  # "light", "dark", "auto"
    language = Column(String, default="en")  # "en", "es", "fr"
    timezone = Column(String, default="UTC")  # User's timezone
    notifications_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    calculation_history_limit = Column(Integer, default=100)  # How many calculations to keep
    auto_save_calculations = Column(Boolean, default=True)
    
    # METADATA FIELDS
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # RELATIONSHIPS
    calculations = relationship("Calculation", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")