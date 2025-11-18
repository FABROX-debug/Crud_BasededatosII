# ui/pacientes_form.py - VERSIÓN CORREGIDA
import tkinter as tk
from tkinter import ttk, messagebox
import re

from models.pacientes import listar_pacientes, crear_paciente, actualizar_paciente, eliminar_paciente


class PacientesForm(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Pacientes")
        self.master.geometry("900x600")

        self.id_paciente_seleccionado = None

        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        tk.Label(self.master, text="Gestión de Pacientes",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        frm = tk.Frame(self.master)
        frm.pack(pady=10)

        # FORMULARIO
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

        # BOTONES
        btns = tk.Frame(self.master)
        btns.pack(pady=10)

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar_form).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # TABLA
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
        self.tree.column("Correo", width=220)
        self.tree.column("Telefono", width=120)

        self.tree.pack(fill="both", pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_tabla(self):
        """Carga todos los pacientes con TODOS sus campos"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            pacientes = listar_pacientes()
            for p in pacientes:
                self.tree.insert("", tk.END, values=p)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes:\n{e}")

    def seleccionar_fila(self, event):
        try:
            item = self.tree.selection()[0]
            vals = self.tree.item(item, "values")
        except:
            return

        self.id_paciente_seleccionado = vals[0]

        # Rellenar formulario
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)

        self.txt_dni.insert(0, vals[1])
        self.txt_nombre.insert(0, vals[2])
        self.txt_correo.insert(0, vals[3])
        self.txt_telefono.insert(0, vals[4])

    def limpiar_form(self):
        self.id_paciente_seleccionado = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)

    def validar_datos(self):
        """Validación mejorada de datos"""
        dni = self.txt_dni.get().strip()
        nombre = self.txt_nombre.get().strip()
        correo = self.txt_correo.get().strip()
        telefono = self.txt_telefono.get().strip()

        # Validar DNI
        if len(dni) != 8 or not dni.isdigit():
            messagebox.showwarning("Error", "El DNI debe tener exactamente 8 dígitos numéricos.")
            return False

        # Validar nombre
        if nombre == "" or len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener al menos 3 caracteres.")
            return False

        # Validar correo (opcional pero si se ingresa debe ser válido)
        if correo != "":
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, correo):
                messagebox.showwarning("Error", "El correo electrónico no tiene un formato válido.")
                return False

        # Validar teléfono (opcional pero si se ingresa debe ser válido)
        if telefono != "":
            if not telefono.isdigit() or len(telefono) < 7:
                messagebox.showwarning("Error", "El teléfono debe contener al menos 7 dígitos.")
                return False

        return True

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
                messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            else:
                actualizar_paciente(self.id_paciente_seleccionado, data)
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")

            self.cargar_tabla()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el paciente:\n{e}")

    def eliminar(self):
        if self.id_paciente_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un paciente para eliminar.")
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar este paciente?\nEsta acción no se puede deshacer."
        )

        if not respuesta:
            return

        try:
            eliminar_paciente(self.id_paciente_seleccionado)
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
            self.cargar_tabla()
            self.limpiar_form()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el paciente:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PacientesForm(master=root)
    root.mainloop()