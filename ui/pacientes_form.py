# ui/pacientes_form.py
# ---------------------------------------------
# Listado simple de pacientes (solo lectura)
# ---------------------------------------------

import tkinter as tk
from tkinter import ttk
from models.pacientes import listar_pacientes

class PacientesForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Pacientes registrados")
        self.master.geometry("600x400")

        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        tk.Label(self.master, text="Pacientes registrados",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self.master,
            columns=("ID", "Nombre", "DNI"),
            show="headings",
            height=15
        )
        self.tree.heading(0, text="ID Paciente")
        self.tree.heading(1, text="Nombre completo")
        self.tree.heading(2, text="DNI")
        self.tree.column(0, width=100)
        self.tree.column(1, width=330)
        self.tree.column(2, width=120)

        self.tree.pack(pady=10, fill="both", expand=True)

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pacientes = listar_pacientes()
        for p in pacientes:
            self.tree.insert("", tk.END, values=p)


# Para probar aislado
if __name__ == "__main__":
    root = tk.Tk()
    app = PacientesForm(master=root)
    app.mainloop()
