# ui/dashboard.py
# -----------------------------------------------------------
# DASHBOARD AVANZADO DE TKINTER
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from models.citas import listar_citas
from utils.styles import apply_styles, BACKGROUND_COLOR, PRIMARY_COLOR


class Dashboard(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Sistema de Reserva de Citas Médicas")
        self.master.geometry("1050x650")

        apply_styles(self.master)
        self.create_widgets()
        self.cargar_citas()

    # -------------------------------------------------------
    def create_widgets(self):
        header = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        header.pack(fill="x", pady=(10, 0))
        tk.Label(header, text="Dashboard", font=("Segoe UI", 18, "bold"), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR).pack()
        tk.Label(header, text="Próximas citas", font=("Segoe UI", 10), bg=BACKGROUND_COLOR).pack()

        tabla_frame = ttk.Frame(self.master, style="Card.TFrame", padding=14)
        tabla_frame.pack(pady=14, padx=14, fill="both", expand=True)

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Paciente", "Medico", "Especialidad", "Fecha", "Hora", "Estado", "Pago"),
            show="headings",
            height=15,
        )

        headers = ["ID", "Paciente", "Médico", "Especialidad", "Fecha", "Hora", "Estado Cita", "Estado Pago"]
        for i, col in enumerate(headers):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=130)

        self.tree.pack(pady=5, fill="both", expand=True)

    # -------------------------------------------------------
    def cargar_citas(self):
        registros = listar_citas()
        for row in registros:
            self.tree.insert("", tk.END, values=row)


# MAIN PARA TESTEAR
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(master=root)
    app.mainloop()
