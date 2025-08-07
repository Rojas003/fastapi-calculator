from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CalculationCreate(BaseModel):
    operation: str
    num1: float
    num2: float

class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    num1: Optional[float] = None
    num2: Optional[float] = None

class CalculationResponse(BaseModel):
    id: int
    operation: str
    num1: float
    num2: float
    result: float
    created_at: datetime
    user_id: int

class CalculationResponse(BaseModel):
    ...
    class Config:
        from_attributes = True
