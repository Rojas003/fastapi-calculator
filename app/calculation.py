from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.calculation import Calculation
from schemas.calculation import CalculationCreate

def create_calculation(calculation: CalculationCreate, db: Session):
    # Compute result based on calculation type
    if calculation.type == "Add":
        result = calculation.a + calculation.b
    elif calculation.type == "Subtract":
        result = calculation.a - calculation.b
    elif calculation.type == "Multiply":
        result = calculation.a * calculation.b
    elif calculation.type == "Divide":
        if calculation.b == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        result = calculation.a / calculation.b
    else:
        raise HTTPException(status_code=400, detail="Invalid calculation type")

    # Create a new Calculation instance (user_id is bypassed or set to None)
    db_calculation = Calculation(
        a=calculation.a,
        b=calculation.b,
        type=calculation.type,
        result=result,
        user_id=None  # Bypassing authentication
    )

    # Save to database
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)

    return db_calculation
