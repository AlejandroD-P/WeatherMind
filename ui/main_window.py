import customtkinter as ctk

from database.db import initialize_database
from database.repository import save_history
from ui.history_panel import HistoryPanel

from datetime import datetime

from services.geocoding_api import get_coordinates

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
        
        initialize_database()
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

        self.history_panel=HistoryPanel(self)

        self.history_panel.grid(

            row=4,

            column=0,

            padx=30,

            pady=15,

            sticky="ew"

        )
    def _set_status(self, text: str, text_color: str = "#a0a0a0"):
        """Actualiza el mensaje de estado central de la interfaz."""
        if hasattr(self, "status_label"):
            self.status_label.configure(text=text, text_color=text_color)
            self.update_idletasks()

    def search_weather(self, *args, **kwargs):
        city_raw = self.city_entry.get() if hasattr(self, "city_entry") else ""
        if isinstance(city_raw, (list, tuple)):
            city_raw = str(city_raw[0]) if city_raw else ""
        city = str(city_raw).strip()

        if not city:
            self._set_status("Por favor, ingrese el nombre de una ciudad.", "#e74c3c")
            return

        if hasattr(self, "search_button"):
            self.search_button.configure(state="disabled", text="Buscando...")
        self._set_status(f"Consultando información para '{city}'...", "#3498db")

        activity = self.activity_combobox.get() if hasattr(self, "activity_combobox") else "Senderismo"

        try:
            coords = get_coordinates(city)
            if not coords:
                self._set_status(f"No se encontró la ubicación: '{city}'. Verifique la ortografía.", "#e74c3c")
                return

            lat, lon = coords[0], coords[1]
            city_display = str(coords[2]) if len(coords) >= 3 else city

            weather_data = get_weather(coords)
            if not weather_data:
                self._set_status("No se pudieron obtener los datos meteorológicos. Revise su conexión.", "#e74c3c")
                return

            weather_data.city = city_display

            if hasattr(self, "weather_panel"):
                self.weather_panel.update_weather(weather_data)

            rec = generate_recommendation(activity, weather_data)
            if hasattr(self, "recommendation_panel"):
                self.recommendation_panel.update_recommendation(rec)

            from database.repository import save_history
            from datetime import datetime

            current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            save_history(current_date, city_display, activity, weather_data, rec)

            if hasattr(self, "history_panel") and hasattr(self.history_panel, "refresh"):
                self.history_panel.refresh()

            self._set_status(f"Consulta actualizada con éxito para {city_display}.", "#2ecc71")

        except Exception as e:
            self._set_status(f"Error inesperado al consultar: {e}", "#e74c3c")
        finally:
            if hasattr(self, "search_button"):
                self.search_button.configure(state="normal", text="Consultar")