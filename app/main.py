# main.py
from fastapi import Depends, FastAPI, HTTPException
from app.database import get_db
from app.schemas.calculation import CalculationCreate, CalculationRead
from app.crud.calculation import create_calculation
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from fastapi.exceptions import RequestValidationError
from app.operations import add, subtract, multiply, divide
from app.database import Base, engine  
from app.models.user import User       
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserRead
from app.utils.security import hash_password
from app.utils.security import hash_password
from app.routes.user_routes import router as user_router
from app.routes import calculation_routes
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()  
app.include_router(calculation_routes.router)
app.include_router(user_router)

import uvicorn
import logging

@app.post("/calculations/", response_model=CalculationRead)
def create_new_calculation(calc: CalculationCreate, db: Session = Depends(get_db)):
    try:
        return create_calculation(db, calc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
print("✅ /calculations route is loaded")
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Pydantic model for request data
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')  # Correct decorator for Pydantic 1.x
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")

# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extracting error messages
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )

@app.get("/")
async def read_root(request: Request):
    """
    Serve the index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e:
        logger.error(f"Divide Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Divide Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
Base.metadata.create_all(bind=engine)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


