from langchain_core.tools import tool

from utils.calculator import Calculator

_calc = Calculator()


@tool
def calculate(operation: str, a: float, b: float) -> float:
    """
    Perform a basic arithmetic operation useful for travel budget calculations.

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'.
        a:         First operand.
        b:         Second operand.

    Returns:
        Result of the arithmetic operation as a float.
    """
    operation = operation.lower().strip()
    ops = {
        "add": _calc.add,
        "subtract": _calc.subtract,
        "multiply": _calc.multiply,
        "divide": _calc.divide,
    }
    if operation not in ops:
        raise ValueError(
            f"Unsupported operation '{operation}'. "
            f"Choose from: {list(ops.keys())}."
        )
    return ops[operation](a, b)


@tool
def calculate_percentage(value: float, pct: float) -> float:
    """
    Compute a percentage of a value (e.g. tip, tax, discount).

    Args:
        value: The base amount.
        pct:   Percentage to compute (e.g. 15 for 15%).

    Returns:
        The percentage portion as a float.
    """
    return _calc.percentage(value, pct)


@tool
def calculate_total_with_tax(value: float, tax_pct: float) -> float:
    """
    Add a tax or service charge percentage on top of a base value.

    Args:
        value:   The pre-tax amount.
        tax_pct: Tax percentage (e.g. 18 for 18% GST).

    Returns:
        The total amount including tax.
    """
    return _calc.total_with_tax(value, tax_pct)