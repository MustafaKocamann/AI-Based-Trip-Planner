from __future__ import annotations

from langchain_core.tools import tool

from utils.weather_info import WeatherInfo


def _get_weather() -> WeatherInfo:
    """Lazily create the WeatherInfo singleton (avoids EnvironmentError on import)."""
    return WeatherInfo()


@tool
def get_current_weather(city: str) -> dict:
    """
    Get the current weather conditions for a city.

    Args:
        city: The name of the city (e.g. 'Paris' or 'New York,US').

    Returns:
        Dictionary with temperature (°C), humidity, description, and wind speed.
    """
    return _get_weather().get_current_weather(city)


@tool
def get_weather_forecast(city: str, days: int = 5) -> list:
    """
    Get a multi-day weather forecast for a city.

    Args:
        city: The name of the city (e.g. 'Tokyo').
        days: Number of forecast days (1–5).

    Returns:
        List of daily forecast entries with avg/min/max temperature in °C.
    """
    return _get_weather().get_forecast_weather(city, days)
