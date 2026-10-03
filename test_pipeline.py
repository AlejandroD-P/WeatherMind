import unittest
import os
import sys
import inspect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.geocoding_api import get_coordinates
from services.weather_api import get_weather
from logic.recommendation_engine import generate_recommendation
from models.recommendation import Recommendation
from models.weather_data import WeatherData
from database.repository import save_history, get_last_history


def create_dummy_weather(city_name="TestCity", temp=22.0, condition="Despejado"):
    """Crea una instancia de WeatherData adaptada a los parámetros exactos de su __init__."""
    sig = inspect.signature(WeatherData.__init__)
    params = list(sig.parameters.keys())[1:]  # omitir 'self'

    defaults = {
        "city": city_name,
        "temperature": float(temp),
        "condition": condition,
        "humidity": 45.0,
        "wind_speed": 10.0,
        "uv_index": 4.0,
        "precipitation_probability": 0.0,
        "precipitation": 0.0,
        "pressure": 1013.2
    }

    kwargs = {p: defaults.get(p, 0.0) for p in params}
    return WeatherData(**kwargs)


class TestWeatherMindPipeline(unittest.TestCase):

    def test_01_geocoding_valid_and_invalid(self):
        """Valida que la geocodificación maneje entradas válidas y vacías."""
        coords = get_coordinates("Monterrey")
        self.assertIsNotNone(coords, "No se obtuvieron coordenadas para Monterrey")
        self.assertGreaterEqual(len(coords), 3, "La tupla debe contener al menos lat, lon y nombre")
        lat, lon = coords[0], coords[1]
        self.assertIsInstance(lat, float)
        self.assertIsInstance(lon, float)

        self.assertIsNone(get_coordinates(""), "Una entrada vacía debe retornar None")
        self.assertIsNone(get_coordinates("   "), "Espacios en blanco deben retornar None")

    def test_02_weather_api_model(self):
        """Valida que la consulta meteorológica retorne una instancia válida de WeatherData."""
        test_coords = (21.018, -101.259, "Guanajuato, México")
        weather = get_weather(test_coords)

        self.assertIsNotNone(weather, "No se obtuvieron datos meteorológicos")
        self.assertIsInstance(weather, WeatherData, "El resultado debe ser una instancia de WeatherData")
        self.assertIsInstance(weather.temperature, float)
        self.assertIsInstance(weather.humidity, float)
        self.assertIsInstance(weather.wind_speed, float)
        self.assertIsInstance(weather.condition, str)

    def test_03_recommendation_engine(self):
        """Valida que el motor de inferencia retorne la dataclass Recommendation completa."""
        dummy_weather = create_dummy_weather(city_name="Ciudad de Prueba", temp=22.0)
        rec = generate_recommendation("Senderismo", dummy_weather)

        self.assertIsInstance(rec, Recommendation, "Debe retornar una instancia de Recommendation")
        self.assertIn(rec.risk_level, ["Bajo", "Moderado", "Alto"])
        self.assertTrue(len(rec.message) > 0, "El mensaje de recomendación no debe estar vacío")
        self.assertTrue(hasattr(rec, "color"), "El objeto debe tener el atributo de color para la UI")

    def test_04_database_persistence(self):
        """Valida que la inserción en SQLite guarde y recupere registros coherentemente."""
        from datetime import datetime
        fecha_test = datetime.now().strftime("%d/%m/%Y %H:%M")
        ciudad_test = "TestCity"
        actividad_test = "Senderismo"

        dummy_weather = create_dummy_weather(city_name=ciudad_test, temp=25.5)
        dummy_rec = Recommendation(
            risk_level="Bajo",
            status="Recomendado",
            message="Condiciones óptimas."
        )

        save_history(fecha_test, ciudad_test, actividad_test, dummy_weather, dummy_rec)

        historial = get_last_history()
        self.assertIsInstance(historial, list, "El historial debe retornar una lista de registros")
        self.assertGreater(len(historial), 0, "Debe existir al menos un registro en la BD")

        ultimo = historial[0]
        self.assertIn(ciudad_test, str(ultimo[1]))
        self.assertEqual(str(ultimo[2]), actividad_test)


if __name__ == "__main__":
    unittest.main()