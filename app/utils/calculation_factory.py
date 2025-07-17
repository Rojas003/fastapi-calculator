# app/utils/calculation_factory.py

from typing import Callable


def add(a: float, b: float) -> float:
    return a + b

def sub(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


class CalculationFactory:
    operations: dict[str, Callable[[float, float], float]] = {
        "Add": add,
        "Sub": sub,
        "Multiply": multiply,
        "Divide": divide,
    }

    @classmethod
    def get_operation(cls, op_type: str) -> Callable[[float, float], float]:
        if op_type not in cls.operations:
            raise ValueError(f"Unsupported operation type: {op_type}")
        return cls.operations[op_type]
