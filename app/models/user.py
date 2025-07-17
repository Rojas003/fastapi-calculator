from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base
# app/user.py

from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    calculations = relationship("Calculation", back_populates="user")

