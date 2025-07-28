from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator
import uvicorn
import logging

# Initialize FastAPI app
app = FastAPI()

# Import and include routers AFTER app is created
from app.routes.user_routes import router as user_router
from app.routes import calculation_routes
app.include_router(user_router)
app.include_router(calculation_routes.router)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Jinja2 templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Import project modules
from app.database import get_db, Base, engine
from app.routes.user_routes import router as user_router
from app.routes import calculation_routes
from app.schemas.calculation import CalculationCreate, CalculationRead
from app.crud.calculation import create_calculation
from app.operations import add, subtract, multiply, divide

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router)
app.include_router(calculation_routes.router)

# Serve HTML pages
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(status_code=400, content={"error": error_messages})

# Input model for operations
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

class OperationResponse(BaseModel):
    result: float

class ErrorResponse(BaseModel):
    error: str

# Calculation API endpoints
@app.post("/calculations/", response_model=CalculationRead)
def create_new_calculation(calc: CalculationCreate, db: Session = Depends(get_db)):
    try:
        return create_calculation(db, calc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    try:
        return OperationResponse(result=add(operation.a, operation.b))
    except Exception as e:
        logger.error(f"Add Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    try:
        return OperationResponse(result=subtract(operation.a, operation.b))
    except Exception as e:
        logger.error(f"Subtract Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    try:
        return OperationResponse(result=multiply(operation.a, operation.b))
    except Exception as e:
        logger.error(f"Multiply Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    try:
        return OperationResponse(result=divide(operation.a, operation.b))
    except ValueError as e:
        logger.error(f"Divide Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal Divide Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
