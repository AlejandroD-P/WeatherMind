import customtkinter as ctk
from database.repository import get_filtered_history, clear_history
from app.constants import ACTIVITIES

class HistoryPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Contenedor superior para el título y botón de borrar
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.title = ctk.CTkLabel(
            self.top_frame,
            text="Historial",
            font=("Arial", 22, "bold"),
            text_color="#3498db"
        )
        self.title.pack(side="left")

        self.clear_btn = ctk.CTkButton(
            self.top_frame,
            text="Borrar Historial",
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.clear_all
        )
        self.clear_btn.pack(side="right")

        # Contenedor para los filtros
        self.filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(fill="x", padx=20, pady=5)

        self.filter_activity = ctk.CTkComboBox(
            self.filter_frame,
            values=["Todas"] + ACTIVITIES,
            width=140,
            command=self.refresh
        )
        self.filter_activity.set("Todas")
        self.filter_activity.pack(side="left", padx=(0, 10))

        self.filter_risk = ctk.CTkComboBox(
            self.filter_frame,
            values=["Todos", "Bajo", "Moderado", "Alto"],
            width=110,
            command=self.refresh
        )
        self.filter_risk.set("Todos")
        self.filter_risk.pack(side="left")

        # Caja de texto del historial
        self.box = ctk.CTkTextbox(self, height=170)
        self.box.pack(padx=20, pady=10, fill="both", expand=True)

        self.refresh()

    def clear_all(self):
        clear_history()
        self.refresh()

    def refresh(self, *args):
        self.box.configure(state="normal")
        self.box.delete("1.0", "end")

        act_val = self.filter_activity.get()
        risk_val = self.filter_risk.get()

        history = get_filtered_history(activity=act_val, risk=risk_val)

        if len(history) == 0:
            self.box.insert("end", "No hay registros que coincidan con los filtros.")
        else:
            for row in history:
                self.box.insert(
                    "end",
                    f"\n{row[0]}\n📍 {row[1]}\n🚶 {row[2]}\n🌡️ {row[3]}°C\n⚠️ Riesgo {row[4]}\n------------------------------------\n"
                )
        self.box.configure(state="disabled")