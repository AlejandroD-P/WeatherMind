import customtkinter as ctk
from datetime import datetime

class ForecastPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title_label = ctk.CTkLabel(self, text="PRONÓSTICO 7 DÍAS", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(10, 5))
        
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def update_forecast(self, daily_forecast, best_day):
        # Limpiar tarjetas anteriores
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        dias_espanol = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        for i, day_data in enumerate(daily_forecast[:7]):
            is_optimal = (day_data["time"] == best_day)
            
            frame_kwargs = {"border_color": "#2ecc71", "border_width": 2} if is_optimal else {"border_color": "#333333", "border_width": 1}            
            
            card = ctk.CTkFrame(self.cards_frame, corner_radius=10, **frame_kwargs)
            card.grid(row=0, column=i, padx=4, sticky="nsew")
            self.cards_frame.grid_columnconfigure(i, weight=1)

            # Etiqueta verde de día óptimo
            if is_optimal:
                ctk.CTkLabel(card, text="Día óptimo", font=("Arial", 10, "bold"), text_color="#2ecc71").pack(pady=(2,0))

            # Extraer y traducir el día de la semana
            try:
                fecha_obj = datetime.strptime(day_data["time"], "%Y-%m-%d")
                nombre_dia = dias_espanol[fecha_obj.weekday()]
            except ValueError:
                nombre_dia = "Día"

            # Nombre del día
            ctk.CTkLabel(card, text=nombre_dia, font=("Arial", 12, "bold"), text_color="#3498db").pack(pady=(5, 0))
            
            # Fecha corta
            fecha_corta = day_data["time"][5:]
            ctk.CTkLabel(card, text=fecha_corta, font=("Arial", 11)).pack(pady=(0, 5))
            
            # Variables meteorológicas
            ctk.CTkLabel(card, text=f"🌡️ {day_data['temperature']}°C", font=("Arial", 11)).pack()
            ctk.CTkLabel(card, text=f"💨 {day_data.get('wind_speed', 0)} km/h", font=("Arial", 11)).pack()
            ctk.CTkLabel(card, text=f"🌧️ {day_data['precipitation']} mm", font=("Arial", 11)).pack(pady=(0, 5))
            ctk.CTkLabel(card, text=f"💧 {day_data.get('humidity', 50)}%", font=("Arial", 11)).pack(pady=(0, 5))