from sqlalchemy.orm import Session
from app.schemas.calculation import CalculationCreate
from app.models.calculation import Calculation
from app.utils.calculation_factory import CalculationFactory


def create_calculation(db: Session, calc_in: CalculationCreate) -> Calculation:
    # Use the factory to get the appropriate operation class
    operation = CalculationFactory.get_operation(calc_in.type)
    
    # Compute the result using the operation class
    result = operation(calc_in.a, calc_in.b)
    
    # Create a new Calculation model instance
    db_calc = Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result
    )
    
    # Add to session and commit
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    
    return db_calc
