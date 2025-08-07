from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Show all calculations
@router.get("/calculations", response_class=HTMLResponse)
def calculations_page(request: Request):
    return templates.TemplateResponse("calculation.html", {"request": request})

# Add a new calculation
@router.get("/calculations/add", response_class=HTMLResponse)
def add_calculation_page(request: Request):
    return templates.TemplateResponse("calculation_add.html", {"request": request})

# Edit a calculation
@router.get("/calculations/edit/{calc_id}", response_class=HTMLResponse)
def edit_calculation_page(calc_id: int, request: Request):
    return templates.TemplateResponse("calculation_edit.html", {"request": request, "calc_id": calc_id})
