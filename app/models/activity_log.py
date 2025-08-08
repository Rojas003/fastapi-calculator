from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Activity details
    action = Column(String, nullable=False)  # "login", "logout", "calculation", "profile_update", etc.
    category = Column(String, nullable=False)  # "auth", "calculation", "profile", "preferences"
    description = Column(String, nullable=True)  # Human readable description
    details = Column(Text, nullable=True)  # JSON string with additional data
    
    # Request context
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    endpoint = Column(String, nullable=True)  # API endpoint that was called
    
    # Metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    duration_ms = Column(Integer, nullable=True)  # How long the action took
    success = Column(String, default="success")  # "success", "error", "warning"
    
    # Relationships
    user = relationship("User", back_populates="activity_logs")
