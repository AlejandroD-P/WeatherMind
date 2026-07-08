import customtkinter as ctk


class WeatherPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Clima actual",
            font=("Arial", 22, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="w")

        self.city_label = ctk.CTkLabel(self, text="📍 Ciudad: -", font=("Arial", 16))
        self.city_label.grid(row=1, column=0, padx=20, pady=6, sticky="w")

        self.temperature_label = ctk.CTkLabel(self, text="🌡 Temperatura: -", font=("Arial", 16))
        self.temperature_label.grid(row=2, column=0, padx=20, pady=6, sticky="w")

        self.condition_label = ctk.CTkLabel(self, text="☁ Condición: -", font=("Arial", 16))
        self.condition_label.grid(row=3, column=0, padx=20, pady=6, sticky="w")

        self.humidity_label = ctk.CTkLabel(self, text="💧 Humedad: -", font=("Arial", 16))
        self.humidity_label.grid(row=4, column=0, padx=20, pady=6, sticky="w")

        self.wind_label = ctk.CTkLabel(self, text="🌬 Viento: -", font=("Arial", 16))
        self.wind_label.grid(row=5, column=0, padx=20, pady=6, sticky="w")

        self.uv_label = ctk.CTkLabel(self, text="☀ Índice UV: -", font=("Arial", 16))
        self.uv_label.grid(row=6, column=0, padx=20, pady=6, sticky="w")

        self.precipitation_label = ctk.CTkLabel(self, text="🌧 Precipitación: -", font=("Arial", 16))
        self.precipitation_label.grid(row=7, column=0, padx=20, pady=6, sticky="w")

    def update_weather(self, weather):
        self.city_label.configure(text=f"📍 Ciudad: {weather.city}")
        self.temperature_label.configure(text=f"🌡 Temperatura: {weather.temperature} °C")
        self.condition_label.configure(text=f"☁ Condición: {weather.condition}")
        self.humidity_label.configure(text=f"💧 Humedad: {weather.humidity}%")
        self.wind_label.configure(text=f"🌬 Viento: {weather.wind_speed} km/h")
        self.uv_label.configure(text=f"☀ Índice UV: {weather.uv_index}")
        self.precipitation_label.configure(
            text=f"🌧 Precipitación: {weather.precipitation_probability} mm"
        )