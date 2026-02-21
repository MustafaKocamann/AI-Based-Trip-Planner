class Calculator:
    """
    Provides basic arithmetic operations for travel budget and cost calculations.
    All inputs are explicitly cast to float at the boundary to prevent precision
    errors when the LLM passes integer-like strings or int values.
    """

    def add(self, a: float, b: float) -> float:
        """Return a + b."""
        a, b = float(a), float(b)
        return round(a + b, 4)

    def subtract(self, a: float, b: float) -> float:
        """Return a - b."""
        a, b = float(a), float(b)
        return round(a - b, 4)

    def multiply(self, a: float, b: float) -> float:
        """Return a * b."""
        a, b = float(a), float(b)
        return round(a * b, 4)

    def divide(self, a: float, b: float) -> float:
        """
        Return a / b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        a, b = float(a), float(b)
        if b == 0.0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return round(a / b, 4)

    def percentage(self, value: float, pct: float) -> float:
        """
        Return pct% of value.

        Args:
            value: The base amount.
            pct:   Percentage to compute (e.g. 15 for 15%).

        Returns:
            The percentage portion as a float.
        """
        value, pct = float(value), float(pct)
        return round(value * pct / 100, 4)

    def total_with_tax(self, value: float, tax_pct: float) -> float:
        """Return value with tax applied: value + percentage(value, tax_pct)."""
        value, tax_pct = float(value), float(tax_pct)
        return round(value + self.percentage(value, tax_pct), 4)