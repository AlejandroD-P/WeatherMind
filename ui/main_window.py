import customtkinter as ctk

from app.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from app.constants import ACTIVITIES
from services.weather_api import get_weather
from logic.recommendation_engine import generate_recommendation


class WeatherMindApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="WeatherMind",
            font=("Arial", 32, "bold")
        )
        self.title_label.pack(pady=20)

        self.city_entry = ctk.CTkEntry(
            self,
            placeholder_text="Escribe una ciudad",
            width=350
        )
        self.city_entry.pack(pady=10)

        self.activity_combo = ctk.CTkComboBox(
            self,
            values=ACTIVITIES,
            width=350
        )
        self.activity_combo.set("Senderismo")
        self.activity_combo.pack(pady=10)

        self.search_button = ctk.CTkButton(
            self,
            text="Consultar clima",
            command=self.search_weather
        )
        self.search_button.pack(pady=15)

        self.result_box = ctk.CTkTextbox(
            self,
            width=700,
            height=300,
            font=("Arial", 16)
        )
        self.result_box.pack(pady=20)

    def search_weather(self):
        city = self.city_entry.get().strip()
        activity = self.activity_combo.get()

        if not city:
            self.show_message("Escribe una ciudad primero.")
            return

        try:
            weather = get_weather(city)

            if weather is None:
                self.show_message("No se encontró la ciudad.")
                return

            recommendation = generate_recommendation(weather, activity)

            result = f"""
    Ciudad: {weather.city}

    Temperatura: {weather.temperature} °C
    Humedad: {weather.humidity} %
    Viento: {weather.wind_speed} km/h
    Precipitación: {weather.precipitation_probability} mm
    Índice UV: {weather.uv_index}
    Condición: {weather.condition}

    Actividad: {activity}

    Resultado: {recommendation.status}
    Nivel de riesgo: {recommendation.risk_level}

    Recomendación:
    {recommendation.message}
    """

            self.show_message(result)

        except Exception as error:
            self.show_message(
                f"No se pudo consultar el clima.\n\nDetalle técnico:\n{error}"
            )

    def show_message(self, message: str):
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", message)