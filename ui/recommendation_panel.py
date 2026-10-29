import customtkinter as ctk

class RecommendationPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Título del panel
        self.title_label = ctk.CTkLabel(self, text="Recomendación", font=("Roboto", 18, "bold"))
        self.title_label.pack(pady=(15, 5))

        # Indicador de Nivel de Confianza
        self.confidence_label = ctk.CTkLabel(self, text="Nivel de Confianza: 0%", font=("Roboto", 12))
        self.confidence_label.pack(pady=(5, 0))

        self.confidence_bar = ctk.CTkProgressBar(self, width=250, progress_color="#2FA572")
        self.confidence_bar.set(0) # Inicializa en 0 (rango de 0.0 a 1.0)
        self.confidence_bar.pack(pady=(5, 10))

        # Cuadro de texto para la explicación de la IA
        self.explanation_box = ctk.CTkTextbox(self, height=100, wrap="word", font=("Arial", 15))
        self.explanation_box.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        self.explanation_box.insert("0.0", "Esperando datos del pronóstico...")
        self.explanation_box.configure(state="disabled") # Bloqueado para solo lectura

    def update_recommendation(self, confidence_score, explanation_text, risk_level="Bajo"):
            # Actualizar barra y porcentaje (asumiendo confidence_score de 0.0 a 1.0)
            percentage = int(confidence_score * 100)
            self.confidence_label.configure(text=f"Nivel de Confianza: {percentage}%")
            self.confidence_bar.set(confidence_score)

            # Cambiar color según riesgo de la barra
            if confidence_score > 0.7:
                self.confidence_bar.configure(progress_color="#2FA572") # Verde
            elif confidence_score > 0.4:
                self.confidence_bar.configure(progress_color="#F39C12") # Amarillo
            else:
                self.confidence_bar.configure(progress_color="#E74C3C") # Rojo

            # Colores tenues para el fondo de la caja de texto
            bg_colors = {
                "Bajo": "#1a3b2b",      # Verde oscuro
                "Moderado": "#423118",  # Café/Naranja oscuro
                "Alto": "#3b1a1a"       # Rojo oscuro
            }
            color_fondo = bg_colors.get(risk_level, "transparent")

            # Actualizar texto explicativo con el nuevo fondo
            self.explanation_box.configure(state="normal", fg_color=color_fondo)
            self.explanation_box.delete("1.0", "end")
            self.explanation_box.insert("1.0", explanation_text)
            self.explanation_box.configure(state="disabled")