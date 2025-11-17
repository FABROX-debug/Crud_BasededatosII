# ui/medicos_form.py
# ---------------------------------------------
# Listado simple de médicos (solo lectura)
# ---------------------------------------------

import tkinter as tk
from tkinter import ttk
from models.medicos import listar_medicos
from utils.styles import apply_styles, BACKGROUND_COLOR, PRIMARY_COLOR


class MedicosForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Médicos registrados")
        self.master.geometry("620x420")

        apply_styles(self.master)
        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        header = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        header.pack(fill="x", pady=10)
        tk.Label(self.master, text="Médicos registrados",
                 font=("Segoe UI", 16, "bold"), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR).pack(pady=(5, 0))

        tabla_wrapper = ttk.Frame(self.master, style="Card.TFrame", padding=12)
        tabla_wrapper.pack(pady=10, padx=12, fill="both", expand=True)

        self.tree = ttk.Treeview(
            tabla_wrapper,
            columns=("ID", "Nombre"),
            show="headings",
            height=15,
        )
        self.tree.heading(0, text="ID Médico")
        self.tree.heading(1, text="Nombre completo")
        self.tree.column(0, width=120)
        self.tree.column(1, width=380)

        self.tree.pack(pady=6, fill="both", expand=True)

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        medicos = listar_medicos()
        for m in medicos:
            self.tree.insert("", tk.END, values=m)


# Para probar aislado
if __name__ == "__main__":
    root = tk.Tk()
    app = MedicosForm(master=root)
    app.mainloop()
