import unittest
from models.weather_data import WeatherData
from logic.recommendation_engine import generate_recommendation

class TestRecommendationEngine(unittest.TestCase):
    
    def test_filtro_dinamico_carretera(self):

        clima_simulado = WeatherData(
            city="Ciudad de Prueba",
            temperature=22.0,
            humidity=99.0,         
            wind_speed=15.0,
            precipitation_probability=0.0,
            uv_index=2.0,
            condition="Nublado",
            pressure=1015.0,
            precipitation=0.0,
            hourly_forecast=[],
            daily_forecast=[]
        )
        
        resultado = generate_recommendation("Viaje por carretera", clima_simulado)
        
        self.assertNotEqual(resultado.risk_level, "Alto", "Error: El filtro dinámico no sobreescribió la humedad.")
        print(f"\n[ÉXITO] Prueba de sobreescritura de reglas lógicas. Riesgo final asignado: {resultado.risk_level}")

if __name__ == '__main__':
    unittest.main()