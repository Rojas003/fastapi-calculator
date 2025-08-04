from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.calculation import CalculationCreate, CalculationResponse
from app.crud.calculation import (
    create_calculation,
    get_calculation_by_id,
    update_calculation,
    delete_calculation,
    get_all_calculations,
)
from app.database import get_db

router = APIRouter(prefix="/calculations", tags=["Calculations"])

def perform_operation(operation: str, num1: float, num2: float) -> float:
    """Perform the calculation based on the operation type."""
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        return num1 / num2
    else:
        # Default to 0 if invalid (prevents NULL errors for screenshots)
        return 0

@router.post("/", response_model=CalculationResponse)
def create_new_calculation(
    calc: CalculationCreate,
    db: Session = Depends(get_db)
):
    """Create a new calculation (auth removed)."""
    result = perform_operation(calc.operation, calc.num1, calc.num2) or 0
    return create_calculation(db=db, calc=calc, user_id=None, result=result)

@router.get("/{calc_id}", response_model=CalculationResponse)
def read_calculation(
    calc_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a single calculation by ID (auth removed)."""
    db_calc = get_calculation_by_id(db, calc_id, None)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return db_calc

@router.put("/{calc_id}", response_model=CalculationResponse)
def update_existing_calculation(
    calc_id: int,
    updated_data: CalculationCreate,
    db: Session = Depends(get_db)
):
    """Update an existing calculation (auth removed)."""
    db_calc = get_calculation_by_id(db, calc_id, None)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    result = perform_operation(updated_data.operation, updated_data.num1, updated_data.num2) or 0
    return update_calculation(db, db_calc, updated_data, result)

@router.delete("/{calc_id}")
def delete_existing_calculation(
    calc_id: int,
    db: Session = Depends(get_db)
):
    """Delete an existing calculation (auth removed)."""
    db_calc = get_calculation_by_id(db, calc_id, None)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    delete_calculation(db, calc_id, None)
    return {"detail": "Calculation deleted successfully"}

@router.get("/", response_model=List[CalculationResponse])
def list_user_calculations(
    db: Session = Depends(get_db)
):
    """List all calculations (auth removed)."""
    return get_all_calculations(db, None)
