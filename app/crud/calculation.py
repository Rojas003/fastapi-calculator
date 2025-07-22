from sqlalchemy.orm import Session
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate
def perform_operation(a: float, b: float, op_type: str) -> float:
    if op_type == "Add":
        return a + b
    elif op_type == "Sub":
        return a - b
    elif op_type == "Multiply":
        return a * b
    elif op_type == "Divide":
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    else:
        raise ValueError(f"Unsupported operation type: {op_type}")


def create_calculation(db: Session, calculation: CalculationCreate):
    result = perform_operation(calculation.a, calculation.b, calculation.type)

    new_calc = Calculation(
        a=calculation.a,
        b=calculation.b,
        type=calculation.type,
        result=result,
        user_id=calculation.user_id
    )
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc
