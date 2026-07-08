from dataclasses import dataclass


@dataclass
class WeatherData:
    city: str
    temperature: float
    humidity: float
    wind_speed: float
    precipitation_probability: float
    uv_index: float
    condition: str