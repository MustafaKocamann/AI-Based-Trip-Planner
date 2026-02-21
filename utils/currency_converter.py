import requests


class CurrencyConverter:
    """
    Converts currency amounts using the free Frankfurter API.
    No API key required.
    """

    BASE_URL = "https://api.frankfurter.app/latest"

    def __init__(self) -> None:
        pass

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert an amount from one currency to another.

        Args:
            amount:        The monetary value to convert.
            from_currency: ISO-4217 source currency code (e.g. "USD").
            to_currency:   ISO-4217 target currency code (e.g. "EUR").

        Returns:
            The converted amount as a float.

        Raises:
            ValueError: If the API returns an unexpected response.
            requests.HTTPError: On network / API errors.
        """
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        if from_currency == to_currency:
            return round(amount, 4)

        params = {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
        }
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "rates" not in data or to_currency not in data["rates"]:
            raise ValueError(
                f"Could not retrieve exchange rate for {from_currency} → {to_currency}."
            )

        return round(data["rates"][to_currency], 4)

    def get_supported_currencies(self) -> list[str]:
        """
        Return a list of currency codes supported by the Frankfurter API.
        """
        response = requests.get("https://api.frankfurter.app/currencies", timeout=10)
        response.raise_for_status()
        return list(response.json().keys())