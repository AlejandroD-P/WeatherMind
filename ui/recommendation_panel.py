import customtkinter as ctk

class RecommendationPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#1e1e1e", corner_radius=12)

        self.title_label = ctk.CTkLabel(
            self,
            text="Recomendación",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(15, 8))

        self.risk_badge = ctk.CTkLabel(
            self,
            text="-",
            font=("Arial", 16, "bold"),
            text_color="#ffffff",
            fg_color="#333333",
            corner_radius=8,
            width=220,
            height=34
        )
        self.risk_badge.pack(pady=5)

        self.message_label = ctk.CTkLabel(
            self,
            text="Listo para consultar.",
            font=("Arial", 13),
            text_color="#e0e0e0",
            wraplength=340,
            justify="center"
        )
        self.message_label.pack(padx=20, pady=(15, 20))

    def update_recommendation(self, rec):
        """Muestra el nivel de riesgo, color y la justificación técnica."""
        level = getattr(rec, "risk_level", None) or (rec.get("risk_level") if isinstance(rec, dict) else "-")
        color = getattr(rec, "color", None) or (rec.get("color") if isinstance(rec, dict) else "#333333")
        
        # Extrae el mensaje de justificación sin importar el nombre del atributo
        message = (
            getattr(rec, "message", None)
            or getattr(rec, "recommendation", None)
            or (rec.get("message") if isinstance(rec, dict) else None)
            or (rec.get("recommendation") if isinstance(rec, dict) else "")
        )

        self.risk_badge.configure(
            text=f"Nivel de riesgo: {level}",
            fg_color=color
        )
        self.message_label.configure(text=str(message))