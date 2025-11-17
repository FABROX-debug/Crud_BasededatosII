# ui/dashboard.py
# -----------------------------------------------------------
# DASHBOARD AVANZADO DE TKINTER
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from models.citas import listar_citas

class Dashboard(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Sistema de Reserva de Citas Médicas")
        self.master.geometry("1050x650")

        self.create_widgets()
        self.cargar_citas()

    # -------------------------------------------------------
    def create_widgets(self):
        # Título
        titulo = tk.Label(self.master, text="Dashboard", font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=15)

        # Tabla de próximas citas
        self.tree = ttk.Treeview(
            self.master,
            columns=("ID", "Paciente", "Medico", "Especialidad", "Fecha", "Hora", "Estado", "Pago"),
            show="headings",
            height=15
        )

        headers = ["ID", "Paciente", "Médico", "Especialidad", "Fecha", "Hora", "Estado Cita", "Estado Pago"]
        for i, col in enumerate(headers):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=130)

        self.tree.pack(pady=10, fill="x")

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
