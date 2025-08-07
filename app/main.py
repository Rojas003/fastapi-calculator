from fastapi import FastAPI, Request, HTTPException, Depends, Body, Path
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import logging
import uvicorn

from app.database import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.calculation import router as calculation_router
from app.auth.jwt_bearer import JWTBearer

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app.include_router(user_router, tags=["Users"])
app.include_router(calculation_router, tags=["Calculations"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

calculations_db = {}  # Simple in-memory store for demonstration

# --- Calculation Models ---
class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

# --- Exception Handlers ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(status_code=400, content={"detail": error_messages})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/calculations-page", response_class=HTMLResponse)
async def calculations_page(request: Request):
    return templates.TemplateResponse("calculation.html", {"request": request})

@app.get("/calculate", response_class=HTMLResponse)
async def calculate_page(request: Request):
    return templates.TemplateResponse("calculation.html", {"request": request})

@app.get("/calculations-page/add", response_class=HTMLResponse)
async def add_calculation_page(request: Request):
    return templates.TemplateResponse("calculation_add.html", {"request": request})

@app.get("/calculations-page/edit/{calc_id}", response_class=HTMLResponse)
async def edit_calculation_page(request: Request, calc_id: int):
    return templates.TemplateResponse("calculation_edit.html", {"request": request, "calc_id": calc_id})

@app.get("/add", response_class=HTMLResponse)
async def add_page(request: Request):
    return templates.TemplateResponse("calculation_add.html", {"request": request})

@app.get("/protected", dependencies=[Depends(JWTBearer())])
async def protected_route(payload: dict = Depends(JWTBearer())):
    return {"message": f"Hello user {payload['user_id']}, you have access!"}

# --- Calculation Endpoints ---

@app.post("/calculate")
async def calculate(input_value: float = Body(...)):
    result = input_value ** 0.5
    calc_id = len(calculations_db) + 1
    calculations_db[calc_id] = {"id": calc_id, "input_value": input_value, "result": result}
    return calculations_db[calc_id]

@app.post("/calculations", dependencies=[Depends(JWTBearer())])
async def add_calculation(calc: CalculationRequest):
    if calc.operation == "add":
        result = calc.num1 + calc.num2
    elif calc.operation == "subtract":
        result = calc.num1 - calc.num2
    elif calc.operation == "multiply":
        result = calc.num1 * calc.num2
    elif calc.operation == "division":
        if calc.num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = calc.num1 / calc.num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
    calc_id = len(calculations_db) + 1
    calculations_db[calc_id] = {
        "id": calc_id,
        "num1": calc.num1,
        "num2": calc.num2,
        "operation": calc.operation,
        "result": result,
    }
    return calculations_db[calc_id]

@app.get("/calculations")
async def list_calculations():
    return {"calculations": list(calculations_db.values())}

@app.get("/calculations/{calc_id}")
async def get_calculation(calc_id: int = Path(...)):
    calc = calculations_db.get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

@app.put("/calculations/{calc_id}", dependencies=[Depends(JWTBearer())])
async def update_calculation(
    calc_id: int = Path(...), 
    calc: CalculationRequest = Body(...)
):
    existing = calculations_db.get(calc_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.operation == "add":
        result = calc.num1 + calc.num2
    elif calc.operation == "subtract":
        result = calc.num1 - calc.num2
    elif calc.operation == "multiply":
        result = calc.num1 * calc.num2
    elif calc.operation == "division":
        if calc.num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = calc.num1 / calc.num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
    existing.update({
        "num1": calc.num1,
        "num2": calc.num2,
        "operation": calc.operation,
        "result": result,
    })
    return existing

@app.delete("/calculations/{calc_id}")
async def delete_calculation(calc_id: int = Path(...)):
    if calc_id not in calculations_db:
        raise HTTPException(status_code=404, detail="Calculation not found")
    del calculations_db[calc_id]
    return {"detail": "Calculation deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
