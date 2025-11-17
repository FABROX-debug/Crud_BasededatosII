# ui/pacientes_form.py
# ---------------------------------------------
# Listado simple de pacientes (solo lectura)
# ---------------------------------------------

import tkinter as tk
from tkinter import ttk
from models.pacientes import listar_pacientes
from utils.styles import apply_styles, BACKGROUND_COLOR, PRIMARY_COLOR


class PacientesForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Pacientes registrados")
        self.master.geometry("620x420")

        apply_styles(self.master)
        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        tk.Label(self.master, text="Pacientes registrados",
                 font=("Segoe UI", 16, "bold"), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR).pack(pady=10)

        tabla_wrapper = ttk.Frame(self.master, style="Card.TFrame", padding=12)
        tabla_wrapper.pack(pady=10, padx=12, fill="both", expand=True)

        self.tree = ttk.Treeview(
            tabla_wrapper,
            columns=("ID", "Nombre"),
            show="headings",
            height=15,
        )
        self.tree.heading(0, text="ID Paciente")
        self.tree.heading(1, text="Nombre completo")
        self.tree.column(0, width=120)
        self.tree.column(1, width=380)

        self.tree.pack(pady=6, fill="both", expand=True)

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
