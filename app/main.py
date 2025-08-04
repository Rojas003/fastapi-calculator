from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
import uvicorn
import logging

from app.database import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.calculation import router as calculation_router
from app.auth.jwt_bearer import JWTBearer  # <-- Import JWTBearer

# Create FastAPI app
app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router, tags=["Users"])
# Secure calculation routes with JWT
app.include_router(
    calculation_router,
    tags=["Calculations"],
    dependencies=[Depends(JWTBearer())]  # <-- Add JWT protection here
)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- FRONTEND ROUTES ----------
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

@app.get("/calculations-page/add", response_class=HTMLResponse)
async def add_calculation_page(request: Request):
    return templates.TemplateResponse("calculation_add.html", {"request": request})

@app.get("/calculations-page/edit/{calc_id}", response_class=HTMLResponse)
async def edit_calculation_page(request: Request, calc_id: int):
    return templates.TemplateResponse("calculation_edit.html", {"request": request, "calc_id": calc_id})

# ---------- EXCEPTION HANDLERS ----------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(status_code=400, content={"error": error_messages})

# ---------- RUN APP ----------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
