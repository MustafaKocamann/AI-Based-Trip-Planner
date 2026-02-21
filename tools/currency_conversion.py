from langchain_core.tools import tool

from utils.currency_converter import CurrencyConverter

_converter = CurrencyConverter()


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convert an amount of money from one currency to another.

    Args:
        amount:        The monetary value to convert.
        from_currency: ISO-4217 source currency code (e.g. 'USD').
        to_currency:   ISO-4217 target currency code (e.g. 'EUR').

    Returns:
        The converted amount as a float.
    """
    return _converter.convert(amount, from_currency, to_currency)