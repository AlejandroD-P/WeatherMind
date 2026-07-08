import requests

from models.weather_data import WeatherData
from services.geocoding_api import get_coordinates


def get_weather(city: str) -> WeatherData | None:
    location = get_coordinates(city)

    if location is None:
        return None

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "precipitation",
            "weather_code"
        ],
        "daily": "uv_index_max",
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    current = data["current"]
    daily = data["daily"]

    return WeatherData(
        city=f'{location["name"]}, {location["country"]}',
        temperature=current["temperature_2m"],
        humidity=current["relative_humidity_2m"],
        wind_speed=current["wind_speed_10m"],
        precipitation_probability=current["precipitation"],
        uv_index=daily["uv_index_max"][0],
        condition=get_weather_condition(current["weather_code"])
    )


def get_weather_condition(code: int) -> str:
    conditions = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos intensos",
        95: "Tormenta",
    }

    return conditions.get(code, "Condición no identificada")