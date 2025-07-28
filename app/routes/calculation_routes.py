from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.calculation import CalculationCreate, CalculationRead
from app.database import get_db
from app.crud import calculation as calculation_crud
from app.auth.jwt_bearer import get_current_user
from app.schemas.user import UserRead

router = APIRouter()

@router.post("/calculate", response_model=CalculationRead)
def create_calculation(
    calculation: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    return calculation_crud.create_calculation(db, calculation, current_user.id)


@router.get("/calculations/{user_id}", response_model=list[CalculationRead])
def get_user_calculations(user_id: int, db: Session = Depends(get_db)):
    return calculation_crud.get_calculations_by_user(db, user_id)


@router.get("/calculation/{calc_id}", response_model=CalculationRead)
def read_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    db_calc = calculation_crud.get_calculation_by_id(db, calc_id)
    if not db_calc or db_calc.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return db_calc


@router.put("/calculation/{calc_id}", response_model=CalculationRead)
def update_calculation(
    calc_id: int,
    updated_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    db_calc = calculation_crud.get_calculation_by_id(db, calc_id)
    if not db_calc or db_calc.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation_crud.update_calculation(db, db_calc, updated_data)


@router.delete("/calculation/{calc_id}")
def delete_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    db_calc = calculation_crud.get_calculation_by_id(db, calc_id)
    if not db_calc or db_calc.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Calculation not found")
    calculation_crud.delete_calculation(db, db_calc)
    return {"detail": "Calculation deleted"}
