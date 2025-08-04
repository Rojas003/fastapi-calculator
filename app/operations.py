# app/operations.py

"""
Module: operations.py

This module contains arithmetic functions (add, subtract, multiply, divide) and a 
single entry point `calculate_result` that determines the correct operation based 
on the provided type.

Functions:
- add(a, b) -> float
- subtract(a, b) -> float
- multiply(a, b) -> float
- divide(a, b) -> float
- calculate_result(a, b, operation_type) -> float
"""

from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> float:
    return a + b

def subtract(a: Number, b: Number) -> float:
    return a - b

def multiply(a: Number, b: Number) -> float:
    return a * b

def divide(a: Number, b: Number) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def calculate_result(a: Number, b: Number, operation_type: str) -> float:
    operation_type = operation_type.capitalize()  # normalize case (e.g. "add" -> "Add")
    if operation_type == "Add":
        return add(a, b)
    elif operation_type == "Subtract":
        return subtract(a, b)
    elif operation_type == "Multiply":
        return multiply(a, b)
    elif operation_type == "Divide":
        return divide(a, b)
    else:
        raise ValueError(f"Invalid operation type: {operation_type}")
