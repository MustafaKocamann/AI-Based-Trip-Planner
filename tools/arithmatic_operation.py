from langchain_core.tools import tool


@tool
def arithmetic_operation(operation: str, a: float, b: float) -> float:
    """
    Perform a simple arithmetic operation.

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'.
        a:         First number.
        b:         Second number.

    Returns:
        Result of the operation as a float.
    """
    operation = operation.lower().strip()

    if operation == "add":
        return round(a + b, 4)
    elif operation == "subtract":
        return round(a - b, 4)
    elif operation == "multiply":
        return round(a * b, 4)
    elif operation == "divide":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return round(a / b, 4)
    else:
        raise ValueError(
            f"Unknown operation '{operation}'. "
            f"Supported: add, subtract, multiply, divide."
        )
