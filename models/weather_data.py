from dataclasses import dataclass, field

@dataclass
class WeatherData:
    city: str
    temperature: float
    humidity: float
    wind_speed: float
    precipitation_probability: float
    uv_index: float
    condition: str
    pressure: float = 1013.2
    precipitation: float = 0.0
    hourly_forecast: list = field(default_factory=list)
    daily_forecast: list = field(default_factory=list)