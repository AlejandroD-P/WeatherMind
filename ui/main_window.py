import customtkinter as ctk

from app.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from app.constants import ACTIVITIES
from services.weather_api import get_weather
from logic.recommendation_engine import generate_recommendation
from ui.weather_panel import WeatherPanel
from ui.recommendation_panel import RecommendationPanel


class WeatherMindApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.header_label = ctk.CTkLabel(
            self,
            text="WeatherMind",
            font=("Arial", 34, "bold")
        )
        self.header_label.grid(row=0, column=0, pady=(25, 10))

        self.search_frame = ctk.CTkFrame(self, corner_radius=15)
        self.search_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_columnconfigure(2, weight=0)

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Escribe una ciudad",
            height=38
        )
        self.city_entry.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        self.activity_combo = ctk.CTkComboBox(
            self.search_frame,
            values=ACTIVITIES,
            height=38
        )
        self.activity_combo.set("Senderismo")
        self.activity_combo.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Consultar",
            height=38,
            command=self.search_weather
        )
        self.search_button.grid(row=0, column=2, padx=15, pady=15)

        self.dashboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard_frame.grid(row=2, column=0, padx=30, pady=20, sticky="nsew")

        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)
        self.dashboard_frame.grid_rowconfigure(0, weight=1)

        self.weather_panel = WeatherPanel(self.dashboard_frame)
        self.weather_panel.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="nsew")

        self.recommendation_panel = RecommendationPanel(self.dashboard_frame)
        self.recommendation_panel.grid(row=0, column=1, padx=(15, 0), pady=10, sticky="nsew")

        self.status_label = ctk.CTkLabel(
            self,
            text="Listo para consultar.",
            font=("Arial", 13)
        )
        self.status_label.grid(row=3, column=0, pady=(0, 15))

    def search_weather(self):
        city = self.city_entry.get().strip()
        activity = self.activity_combo.get()

        if not city:
            self.status_label.configure(text="Escribe una ciudad primero.")
            return

        try:
            self.status_label.configure(text="Consultando clima...")
            self.update_idletasks()

            weather = get_weather(city)

            if weather is None:
                self.status_label.configure(text="No se encontró la ciudad.")
                return

            recommendation = generate_recommendation(weather, activity)

            self.weather_panel.update_weather(weather)
            self.recommendation_panel.update_recommendation(recommendation)

            self.status_label.configure(text="Consulta completada.")

        except Exception as error:
            self.status_label.configure(text=f"No se pudo consultar el clima: {error}")