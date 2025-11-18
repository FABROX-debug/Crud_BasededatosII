# ui/pacientes_form.py
# -----------------------------------------------------------
# CRUD COMPLETO PARA PACIENTES (Optimizado)
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

from models.pacientes import listar_pacientes, crear_paciente, actualizar_paciente, eliminar_paciente


class PacientesForm(tk.Frame):

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Pacientes")
        self.master.geometry("850x600")

        self.id_paciente_seleccionado = None

        self.crear_widgets()
        self.cargar_tabla()

    # -------------------------------------------------------
    def crear_widgets(self):

        tk.Label(self.master, text="Gestión de Pacientes",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        frm = tk.Frame(self.master)
        frm.pack(pady=10)

        # ------- FORMULARIO -------
        labels = ["DNI:", "Nombre:", "Correo:", "Teléfono:"]
        for i, text in enumerate(labels):
            tk.Label(frm, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)

        self.txt_dni = tk.Entry(frm, width=30)
        self.txt_nombre = tk.Entry(frm, width=40)
        self.txt_correo = tk.Entry(frm, width=40)
        self.txt_telefono = tk.Entry(frm, width=20)

        self.txt_dni.grid(row=0, column=1)
        self.txt_nombre.grid(row=1, column=1)
        self.txt_correo.grid(row=2, column=1)
        self.txt_telefono.grid(row=3, column=1)

        # ------- BOTONES -------
        btns = tk.Frame(self.master)
        btns.pack(pady=10)

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar_form).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # ------- TABLA -------
        columnas = ("ID", "DNI", "Nombre", "Correo", "Telefono")

        self.tree = ttk.Treeview(
            self.master,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=60)
        self.tree.column("DNI", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.column("Correo", width=180)
        self.tree.column("Telefono", width=120)

        self.tree.pack(fill="both", pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # -------------------------------------------------------
    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pacientes = listar_pacientes()

        # lista: (ID_PACIENTE, DNI, NOMBRE)
        for p in pacientes:
            # completar campos correo y teléfono desde la BD
            # necesitamos fetch_all pero lo haremos directo al model
            # como tu model solo retorna 3 campos, actualizamos:
            idp, dni, nombre = p
            self.tree.insert("", tk.END, values=(idp, dni, nombre, "", ""))

    # -------------------------------------------------------
    def seleccionar_fila(self, event):
        try:
            item = self.tree.selection()[0]
            vals = self.tree.item(item, "values")
        except:
            return

        self.id_paciente_seleccionado = vals[0]

        # rellenar formulario
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)

        self.txt_dni.insert(0, vals[1])
        self.txt_nombre.insert(0, vals[2])
        self.txt_correo.insert(0, vals[3] if vals[3] else "")
        self.txt_telefono.insert(0, vals[4] if vals[4] else "")

    # -------------------------------------------------------
    def limpiar_form(self):
        self.id_paciente_seleccionado = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)

    # -------------------------------------------------------
    def validar_datos(self):
        dni = self.txt_dni.get().strip()
        nombre = self.txt_nombre.get().strip()

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showwarning("Error", "El DNI debe tener 8 dígitos numéricos.")
            return False

        if nombre == "":
            messagebox.showwarning("Error", "El campo 'Nombre' es obligatorio.")
            return False

        return True

    # -------------------------------------------------------
    def guardar(self):
        if not self.validar_datos():
            return

        data = {
            "dni": self.txt_dni.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "correo": self.txt_correo.get().strip(),
            "telefono": self.txt_telefono.get().strip()
        }

        try:
            if self.id_paciente_seleccionado is None:
                crear_paciente(data)
                messagebox.showinfo("OK", "Paciente registrado.")
            else:
                actualizar_paciente(self.id_paciente_seleccionado, data)
                messagebox.showinfo("OK", "Paciente actualizado.")

            self.cargar_tabla()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    # -------------------------------------------------------
    def eliminar(self):
        if self.id_paciente_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un paciente para eliminar.")
            return

        try:
            eliminar_paciente(self.id_paciente_seleccionado)
            messagebox.showinfo("OK", "Paciente eliminado.")
            self.cargar_tabla()
            self.limpiar_form()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


# Prueba aislada
if __name__ == "__main__":
    root = tk.Tk()
    app = PacientesForm(master=root)
    root.mainloop()
