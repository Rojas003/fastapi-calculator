from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate

def create_calculation(db: Session, calc: CalculationCreate, user_id: int, result: float):
    db_calculation = Calculation(
        num1=calc.num1,
        num2=calc.num2,
        operation=calc.operation,
        result=result,
        user_id=user_id
    )
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    return db_calculation

def get_calculation_by_id(db: Session, calc_id: int, user_id: int):
    return db.query(Calculation).filter(Calculation.id == calc_id, Calculation.user_id == user_id).first()

def update_calculation(db: Session, db_calc: Calculation, updated_data: CalculationCreate, result: float):
    db_calc.num1 = updated_data.num1
    db_calc.num2 = updated_data.num2
    db_calc.operation = updated_data.operation
    db_calc.result = result
    db.commit()
    db.refresh(db_calc)
    return db_calc

def delete_calculation(db: Session, calc_id: int, user_id: int):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.user_id == user_id).first()
    if calc:
        db.delete(calc)
        db.commit()

def get_all_calculations(db: Session, user_id: int):
    return db.query(Calculation).filter(Calculation.user_id == user_id).all()
