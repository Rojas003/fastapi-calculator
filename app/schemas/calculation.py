from pydantic import BaseModel, validator
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


class CalculationResponse(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: Optional[float]
    user_id: Optional[int]  # allow NULL in the response

    class Config:
        from_attributes = True
