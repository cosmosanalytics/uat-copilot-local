"""
math_engine.py
A sample core module to demonstrate real GitHub CI/CD testing and validation.
"""

def add(a: float, b: float) -> float:
    """Returns the sum of a and b."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Returns the product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Returns a divided by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

def compute_compound_interest(principal: float, rate: float, periods: int) -> float:
    """Calculates compound interest: P * (1 + r)^n"""
    if principal < 0 or rate < 0 or periods < 0:
        raise ValueError("Inputs must be non-negative")
    return round(principal * ((1 + rate) ** periods), 2)
