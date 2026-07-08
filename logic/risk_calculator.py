from models.weather_data import WeatherData


def calculate_risk(weather: WeatherData) -> str:
    if weather.precipitation_probability >= 70:
        return "Alto"

    if weather.wind_speed >= 40:
        return "Alto"

    if weather.uv_index >= 9:
        return "Moderado"

    if weather.temperature >= 34:
        return "Moderado"

    return "Bajo"
