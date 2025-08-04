from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth.jwt_bearer import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Show all calculations
@router.get("/calculations", response_class=HTMLResponse)
def calculations_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse("calculations.html", {"request": request, "user": current_user})

# Add a new calculation
@router.get("/calculations/add", response_class=HTMLResponse)
def add_calculation_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse("calculation_add.html", {"request": request, "user": current_user})

# Edit a calculation
@router.get("/calculations/edit/{calc_id}", response_class=HTMLResponse)
def edit_calculation_page(
    calc_id: int,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse("calculation_edit.html", {"request": request, "user": current_user, "calc_id": calc_id})
