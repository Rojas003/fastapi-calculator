from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate

def create_calculation(db: Session, calc: CalculationCreate, user_id: int = None):
    """Create a new calculation and compute result before saving."""

    calculation = Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        user_id=user_id
    )

    try:
        calculation.result = calculation.compute_result()  # ✅ compute result before saving
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation


def get_calculation_by_id(db: Session, calc_id: int, user_id: int = None):
    return db.query(Calculation).filter(Calculation.id == calc_id).first()


def update_calculation(db: Session, db_calc: Calculation, updated_data: CalculationCreate):
    db_calc.a = updated_data.a
    db_calc.b = updated_data.b
    db_calc.type = updated_data.type

    try:
        db_calc.result = db_calc.compute_result()  # ✅ recompute result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db.commit()
    db.refresh(db_calc)
    return db_calc


def delete_calculation(db: Session, calc_id: int, user_id: int = None):
    calc = get_calculation_by_id(db, calc_id, user_id)
    if calc:
        db.delete(calc)
        db.commit()


def get_all_calculations(db: Session, user_id: int = None):
    return db.query(Calculation).all()
