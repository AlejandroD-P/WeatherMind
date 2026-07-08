import customtkinter as ctk


class RecommendationPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Recomendación",
            font=("Arial", 22, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="w")

        self.status_label = ctk.CTkLabel(
            self,
            text="-",
            font=("Arial", 28, "bold")
        )
        self.status_label.grid(row=1, column=0, pady=10, padx=20)

        self.risk_label = ctk.CTkLabel(
            self,
            text="Nivel de riesgo: -",
            font=("Arial", 16)
        )
        self.risk_label.grid(row=2, column=0, pady=8, padx=20)

        self.message_box = ctk.CTkTextbox(
            self,
            width=360,
            height=170,
            font=("Arial", 15),
            wrap="word"
        )
        self.message_box.grid(row=3, column=0, pady=20, padx=20)

    def update_recommendation(self, recommendation):
        risk_icon = {
            "Bajo": "🟢",
            "Moderado": "🟡",
            "Alto": "🔴"
        }.get(recommendation.risk_level, "⚪")

        self.status_label.configure(text=f"{risk_icon} {recommendation.status}")
        self.risk_label.configure(text=f"Nivel de riesgo: {recommendation.risk_level}")

        self.message_box.delete("1.0", "end")
        self.message_box.insert("1.0", recommendation.message)