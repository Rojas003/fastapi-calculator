from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.calculation import Calculation
from app.database import get_db
from app.auth.jwt_bearer import JWTBearer  # Make sure this import is present

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

class CalculationUpdateRequest(BaseModel):
    num1: float
    num2: float
    operation: str

@router.get("/calculations-page/add", response_class=HTMLResponse)
async def get_calculation_page(request: Request):
    return templates.TemplateResponse("calculation.html", {"request": request, "message": ""})

@router.get("/calculations")
async def get_calculations(db: Session = Depends(get_db)):
    calculations = db.query(Calculation).all()
    return {
        "calculations": [
            {"id": calc.id, "num1": calc.a, "num2": calc.b, "operation": calc.type, "result": calc.result}
            for calc in calculations
        ]
    }

@router.post("/calculations", dependencies=[Depends(JWTBearer())])
async def add_calculation(calc: CalculationRequest, db: Session = Depends(get_db)):
    return await perform_calculation(calc, db)

@router.post("/calculate")
async def calculate(calc: CalculationRequest, db: Session = Depends(get_db)):
    return await perform_calculation(calc, db)

async def perform_calculation(calc: CalculationRequest, db: Session):
    operation = calc.operation.strip().lower()
    if operation in ["add", "addition"]:
        result = calc.num1 + calc.num2
    elif operation in ["subtract", "subtraction"]:
        result = calc.num1 - calc.num2
    elif operation in ["multiply", "multiplication"]:
        result = calc.num1 * calc.num2
    elif operation in ["divide", "division"]:
        if calc.num2 == 0:
            return JSONResponse(status_code=400, content={"detail": "Division by zero"})
        result = calc.num1 / calc.num2
    else:
        return JSONResponse(status_code=400, content={"detail": "Invalid operation"})

    calculation = Calculation(a=calc.num1, b=calc.num2, type=operation, result=result)
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return {"id": calculation.id, "num1": calculation.a, "num2": calculation.b, "operation": calculation.type, "result": calculation.result, "message": "Calculation added successfully"}

@router.get("/calculations/{calc_id}")
async def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calculation:
        return JSONResponse(status_code=404, content={"detail": "Calculation not found"})
    return {"id": calculation.id, "num1": calculation.a, "num2": calculation.b, "operation": calculation.type, "result": calculation.result}

@router.put("/calculations/{calc_id}")
async def update_calculation(calc_id: int, calc_update: CalculationUpdateRequest, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calculation:
        return JSONResponse(status_code=404, content={"detail": "Calculation not found"})

    operation = calc_update.operation.strip().lower()
    if operation in ["add", "addition"]:
        result = calc_update.num1 + calc_update.num2
    elif operation in ["subtract", "subtraction"]:
        result = calc_update.num1 - calc_update.num2
    elif operation in ["multiply", "multiplication"]:
        result = calc_update.num1 * calc_update.num2
    elif operation in ["divide", "division"]:
        if calc_update.num2 == 0:
            return JSONResponse(status_code=400, content={"detail": "Division by zero"})
        result = calc_update.num1 / calc_update.num2
    else:
        return JSONResponse(status_code=400, content={"detail": "Invalid operation"})

    calculation.a = calc_update.num1
    calculation.b = calc_update.num2
    calculation.type = operation
    calculation.result = result

    db.commit()
    db.refresh(calculation)
    return {"id": calculation.id, "num1": calculation.a, "num2": calculation.b, "operation": calculation.type, "result": calculation.result, "message": "Calculation updated successfully"}

@router.delete("/calculations/{calc_id}")
async def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calculation:
        return JSONResponse(status_code=404, content={"detail": "Calculation not found"})
    db.delete(calculation)
    db.commit()
    return {"detail": "Calculation deleted successfully"}

@router.get("/calculation/edit/{calc_id}", response_class=HTMLResponse)
async def edit_calculation_page(calc_id: int, request: Request, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calculation:
        return templates.TemplateResponse("calculation.html", {"request": request, "message": "Calculation not found"})
    return templates.TemplateResponse("calculation.html", {"request": request, "calculation": calculation, "message": ""})

@router.get("/register-success", response_class=HTMLResponse)
async def register_success(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "message": "Registered successfully"})

@router.get("/login-success", response_class=HTMLResponse)
async def login_success(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": "Logged in successfully"})
