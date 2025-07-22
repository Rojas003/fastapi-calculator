# app/models/calculation.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class Calculation(Base):
    __tablename__ = "calculations"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    result = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))  
    user = relationship("User", back_populates="calculations")  