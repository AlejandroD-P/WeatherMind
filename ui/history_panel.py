import customtkinter as ctk

from database.repository import get_last_history


class HistoryPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.title=ctk.CTkLabel(
            self,
            text="Historial",
            font=("Arial",22,"bold")
        )

        self.title.pack(pady=15)

        self.box=ctk.CTkTextbox(
            self,
            width=850,
            height=170
        )

        self.box.pack(padx=20,pady=10)

        self.refresh()


    def refresh(self):

        self.box.delete("1.0","end")

        history=get_last_history()

        if len(history)==0:

            self.box.insert(
                "end",
                "Aún no existen consultas."
            )

            return

        for row in history:

            self.box.insert(
                "end",

                f"""
{row[0]}

📍 {row[1]}

🚶 {row[2]}

🌡 {row[3]}°C

⚠ Riesgo {row[4]}

------------------------------------

"""
            )