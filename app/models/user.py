from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Renamed from hashed_password to match usage
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Proper back_populates matches Calculation.user
    calculations = relationship("Calculation", back_populates="user", cascade="all, delete-orphan")
