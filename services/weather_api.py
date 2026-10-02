import urllib.request
import json
from models.weather_data import WeatherData

def get_weather(*args, **kwargs):
    """
    Consulta Open-Meteo Forecast API y construye WeatherData
    con todos los atributos requeridos por el modelo.
    """
    try:
        # 1. Resolver latitud y longitud
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

        # 2. Solicitar variables actuales a Open-Meteo
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current="
            f"temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code,uv_index"
            f"&hourly=precipitation_probability&forecast_days=1"
        )

        req = urllib.request.Request(url, headers={"User-Agent": "WeatherMindApp/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return None
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current", {})
        temp = float(current.get("temperature_2m", 20.0))
        humidity = float(current.get("relative_humidity_2m", 50.0))
        wind = float(current.get("wind_speed_10m", 10.0))
        precip = float(current.get("precipitation", 0.0))
        pressure = float(current.get("surface_pressure", 1013.2))
        code = int(current.get("weather_code", 0))
        uv = float(current.get("uv_index", 5.0))

        # Probabilidad de precipitación tomada de la primera hora disponible
        hourly = data.get("hourly", {})
        prob_list = hourly.get("precipitation_probability", [0])
        precip_prob = float(prob_list[0]) if prob_list else 0.0

        # Traducir código meteorológico a texto legible
        condition_desc = "Despejado"
        if code in [1, 2, 3]:
            condition_desc = "Parcialmente nublado"
        elif code in [45, 48]:
            condition_desc = "Niebla"
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            condition_desc = "Lluvia"
        elif code >= 95:
            condition_desc = "Tormenta eléctrica"

        # 3. Instanciar WeatherData soportando kwargs o argumentos posicionales
        try:
            return WeatherData(
                city="",
                temperature=temp,
                condition=condition_desc,
                humidity=humidity,
                wind_speed=wind,
                pressure=pressure,
                precipitation=precip,
                uv_index=uv,
                precipitation_probability=precip_prob
            )
        except TypeError:
            # Respaldo posicional según el orden habitual de la dataclass
            try:
                return WeatherData(
                    city="",
                    temperature=temp,
                    humidity=humidity,
                    wind_speed=wind,
                    pressure=pressure,
                    precipitation=precip,
                    uv_index=uv,
                    precipitation_probability=precip_prob,
                    condition=condition_desc
                )
            except Exception:
                # Si acepta parámetros dinámicos
                obj = WeatherData.__new__(WeatherData)
                obj.city = ""
                obj.temperature = temp
                obj.condition = condition_desc
                obj.humidity = humidity
                obj.wind_speed = wind
                obj.pressure = pressure
                obj.precipitation = precip
                obj.uv_index = uv
                obj.precipitation_probability = precip_prob
                return obj

    except Exception as e:
        print(f"-> Excepción en get_weather: {e}")
        return None