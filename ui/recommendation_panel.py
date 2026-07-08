import customtkinter as ctk


class RecommendationPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(width=420,height=350)

        self.title=ctk.CTkLabel(
            self,
            text="Recomendación",
            font=("Arial",22,"bold")
        )

        self.title.pack(pady=(20,15))

        self.status=ctk.CTkLabel(
            self,
            text="-",
            font=("Arial",24,"bold")
        )

        self.status.pack(pady=10)

        self.risk=ctk.CTkLabel(
            self,
            text="Riesgo: -"
        )

        self.risk.pack()

        self.message=ctk.CTkTextbox(
            self,
            width=330,
            height=170
        )

        self.message.pack(pady=20)

    def update_recommendation(self,recommendation):

        self.status.configure(
            text=recommendation.status
        )

        self.risk.configure(
            text=f"Nivel de riesgo: {recommendation.risk_level}"
        )

        self.message.delete("1.0","end")

        self.message.insert(
            "1.0",
            recommendation.message
        )