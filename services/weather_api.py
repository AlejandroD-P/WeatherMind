import urllib.request
import json
from models.weather_data import WeatherData

def get_weather(*args, **kwargs):
    try:
        if len(args) == 1:
            first = args[0]
            if isinstance(first, (tuple, list)):
                lat, lon = float(first[0]), float(first[1])
            else:
                lat = float(getattr(first, "latitude", 0.0))
                lon = float(getattr(first, "longitude", 0.0))
        elif len(args) >= 2:
            lat, lon = float(args[0]), float(args[1])
        else:
            lat = float(kwargs.get("lat", kwargs.get("latitude", 0.0)))
            lon = float(kwargs.get("lon", kwargs.get("longitude", 0.0)))

        # URL actualizada para pronóstico extendido de 7 días y variables detalladas por hora/día
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current="
            f"temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code,uv_index"
            f"&hourly=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,precipitation_probability"
            f"&daily=temperature_2m_max,precipitation_sum,wind_speed_10m_max"
            f"&forecast_days=7&timezone=auto"
        )

        req = urllib.request.Request(url, headers={"User-Agent": "WeatherMindApp/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return None
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current", {})
        hourly_data = data.get("hourly", {})
        daily_data = data.get("daily", {})

        temp = float(current.get("temperature_2m", 20.0))
        humidity = float(current.get("relative_humidity_2m", 50.0))
        wind = float(current.get("wind_speed_10m", 10.0))
        precip = float(current.get("precipitation", 0.0))
        pressure = float(current.get("surface_pressure", 1013.2))
        code = int(current.get("weather_code", 0))
        uv = float(current.get("uv_index", 5.0))
        
        prob_list = hourly_data.get("precipitation_probability", [0])
        precip_prob = float(prob_list[0]) if prob_list else 0.0

        # Procesar proyecciones por hora
        hourly_forecast = []
        if "time" in hourly_data:
            for i in range(len(hourly_data["time"])):
                hourly_forecast.append({
                    "time": hourly_data["time"][i],
                    "temperature": hourly_data.get("temperature_2m", [])[i],
                    "humidity": hourly_data.get("relative_humidity_2m", [])[i],
                    "precipitation": hourly_data.get("precipitation", [])[i],
                    "pressure": hourly_data.get("surface_pressure", [])[i],
                    "wind_speed": hourly_data.get("wind_speed_10m", [])[i]
                })
                
        # Procesar proyecciones por día
        daily_forecast = []
        if "time" in daily_data:
            for i in range(len(daily_data["time"])):
                daily_forecast.append({
                    "time": daily_data["time"][i],
                    "temperature": daily_data.get("temperature_2m_max", [])[i],
                    "precipitation": daily_data.get("precipitation_sum", [])[i],
                    "wind_speed": daily_data.get("wind_speed_10m_max", [])[i],
                    "humidity": 50.0, 
                    "pressure": 1013.2
                })

        condition_desc = "Despejado"
        if code in [1, 2, 3]: condition_desc = "Parcialmente nublado"
        elif code in [45, 48]: condition_desc = "Niebla"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: condition_desc = "Lluvia"
        elif code >= 95: condition_desc = "Tormenta eléctrica"

        return WeatherData(
            city="",
            temperature=temp,
            condition=condition_desc,
            humidity=humidity,
            wind_speed=wind,
            pressure=pressure,
            precipitation=precip,
            uv_index=uv,
            precipitation_probability=precip_prob,
            hourly_forecast=hourly_forecast,
            daily_forecast=daily_forecast
        )

    except Exception as e:
        print(f"-> Excepción en get_weather: {e}")
        return None