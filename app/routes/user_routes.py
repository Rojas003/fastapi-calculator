from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.calculation import CalculationCreate, CalculationResponse
from app.models.calculation import Calculation
from app.database import get_db

router = APIRouter()

# CREATE calculation
@router.post("/calculations/", response_model=CalculationResponse)
def create_calculation(calculation: CalculationCreate, db: Session = Depends(get_db)):
    user_id = 1  # Bypass authentication
    new_calc = Calculation(**calculation.dict(), user_id=user_id)
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc

# READ single calculation
@router.get("/calculations/{calc_id}", response_model=CalculationResponse)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

# LIST all calculations
@router.get("/calculations/", response_model=list[CalculationResponse])
def list_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()

# UPDATE calculation
@router.put("/calculations/{calc_id}", response_model=CalculationResponse)
def update_calculation(calc_id: int, calculation: CalculationCreate, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    for key, value in calculation.dict().items():
        setattr(calc, key, value)
    db.commit()
    db.refresh(calc)
    return calc

# DELETE calculation
@router.delete("/calculations/{calc_id}")
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
    return {"message": "Calculation deleted successfully"}
