# ui/medicos_form.py
# ---------------------------------------------
# Listado simple de médicos (solo lectura)
# ---------------------------------------------

import tkinter as tk
from tkinter import ttk
from models.medicos import listar_medicos

class MedicosForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Médicos registrados")
        self.master.geometry("600x400")

        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        tk.Label(self.master, text="Médicos registrados",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self.master,
            columns=("ID", "Nombre"),
            show="headings",
            height=15
        )
        self.tree.heading(0, text="ID Médico")
        self.tree.heading(1, text="Nombre completo")
        self.tree.column(0, width=100)
        self.tree.column(1, width=350)

        self.tree.pack(pady=10, fill="both", expand=True)

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
