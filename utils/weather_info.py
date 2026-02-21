import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherInfo:
    """
    Retrieves current weather and forecast data from OpenWeatherMap.
    All temperatures are returned in Celsius (units='metric').
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise EnvironmentError(
                "OPENWEATHERMAP_API_KEY is not set in environment variables."
            )

    def get_current_weather(self, city: str) -> dict:
        """
        Fetch current weather conditions for a city.

        Args:
            city: City name (e.g. "Paris" or "New York,US").

        Returns:
            Dictionary with keys: city, temperature, feels_like, humidity,
            description, wind_speed, units.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }
        response = requests.get(
            f"{self.BASE_URL}/weather", params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "wind_speed": data["wind"]["speed"],
            "units": "metric",
        }

    def get_forecast_weather(self, city: str, days: int = 5) -> list[dict]:
        """
        Fetch a multi-day weather forecast for a city.

        Args:
            city: City name (e.g. "Tokyo").
            days: Number of days to forecast (1–5; OpenWeatherMap free tier
                  returns up to 5 days in 3-hour intervals).

        Returns:
            List of daily forecast dictionaries, each with keys: date,
            avg_temp, min_temp, max_temp, description, units.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "cnt": 40,  # 40 × 3-hour slots = full 5-day window (OWM max)
        }
        response = requests.get(
            f"{self.BASE_URL}/forecast", params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Aggregate 3-hour intervals into daily summaries
        daily: dict[str, dict] = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            temp = entry["main"]["temp"]
            description = entry["weather"][0]["description"].capitalize()

            if date not in daily:
                daily[date] = {
                    "date": date,
                    "temps": [],
                    "description": description,
                    "units": "metric",
                }
            daily[date]["temps"].append(temp)

        forecast = []
        for day_data in list(daily.values())[:days]:
            temps = day_data.pop("temps")
            day_data["avg_temp"] = round(sum(temps) / len(temps), 1)
            day_data["min_temp"] = round(min(temps), 1)
            day_data["max_temp"] = round(max(temps), 1)
            forecast.append(day_data)

        return forecast