# app/schemas/calculation.py
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: Literal["Add", "Sub", "Multiply", "Divide"]

    @validator("b")
    def validate_divisor(cls, b, values):
        if "type" in values and values["type"] == "Divide" and b == 0:
            raise ValueError("Division by zero is not allowed.")
        return b


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: Optional[float]
    user_id: int

    class Config:
        orm_mode = True
