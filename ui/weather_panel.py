import customtkinter as ctk


class WeatherPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(width=420, height=350)

        self.title = ctk.CTkLabel(
            self,
            text="Clima",
            font=("Arial",22,"bold")
        )
        self.title.pack(pady=(20,15))

        self.city = ctk.CTkLabel(self,text="Ciudad: -")
        self.city.pack(anchor="w",padx=20)

        self.temperature = ctk.CTkLabel(self,text="🌡 Temperatura: -")
        self.temperature.pack(anchor="w",padx=20,pady=5)

        self.condition = ctk.CTkLabel(self,text="☁ Condición: -")
        self.condition.pack(anchor="w",padx=20,pady=5)

        self.humidity = ctk.CTkLabel(self,text="💧 Humedad: -")
        self.humidity.pack(anchor="w",padx=20,pady=5)

        self.wind = ctk.CTkLabel(self,text="🌬 Viento: -")
        self.wind.pack(anchor="w",padx=20,pady=5)

        self.uv = ctk.CTkLabel(self,text="☀ UV: -")
        self.uv.pack(anchor="w",padx=20,pady=5)

    def update_weather(self, weather):

        self.city.configure(
            text=f"{weather.city}"
        )

        self.temperature.configure(
            text=f"{weather.temperature} °C"
        )

        self.condition.configure(
            text=f"{weather.condition}"
        )

        self.humidity.configure(
            text=f"{weather.humidity}%"
        )

        self.wind.configure(
            text=f"{weather.wind_speed} km/h"
        )

        self.uv.configure(
            text=f"UV {weather.uv_index}"
        )