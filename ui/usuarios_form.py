# ui/usuarios_form.py
# -----------------------------------------------------------
# CRUD de Usuarios – Versión Profesional
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

from models.usuarios import (
    listar_usuarios,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario
)


class UsuariosForm(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Usuarios")
        self.master.geometry("900x600")

        self.id_usuario = None

        self.crear_widgets()
        self.cargar_tabla()

    # -------------------------------------------------------
    def crear_widgets(self):

        tk.Label(
            self.master,
            text="Gestión de Usuarios",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # FORMULARIO
        form = tk.Frame(self.master)
        form.pack(pady=10)

        tk.Label(form, text="DNI:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form, text="Nombre completo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form, text="Tipo usuario:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form, text="Contraseña:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form, text="Estado:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.txt_dni = tk.Entry(form, width=25)
        self.txt_nombre = tk.Entry(form, width=40)
        self.cbo_tipo = ttk.Combobox(form, values=["ADMIN", "MEDICO", "PACIENTE"], width=20)
        self.txt_password = tk.Entry(form, width=25, show="*")
        self.cbo_estado = ttk.Combobox(form, values=["S", "N"], width=5)

        self.txt_dni.grid(row=0, column=1, padx=5)
        self.txt_nombre.grid(row=1, column=1, padx=5)
        self.cbo_tipo.grid(row=2, column=1, padx=5)
        self.txt_password.grid(row=3, column=1, padx=5)
        self.cbo_estado.grid(row=4, column=1, padx=5)

        # BOTONES
        btns = tk.Frame(self.master)
        btns.pack()

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # TABLA
        columnas = ("ID", "DNI", "Nombre", "Tipo", "Estado")
        self.tree = ttk.Treeview(
            self.master, columns=columnas, show="headings", height=15
        )

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    # -------------------------------------------------------
    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        datos = listar_usuarios()

        for u in datos:
            self.tree.insert("", tk.END, values=u)

    # -------------------------------------------------------
    def seleccionar(self, event):
        item = self.tree.selection()[0]
        vals = self.tree.item(item, "values")

        self.id_usuario = vals[0]

        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)

        self.txt_dni.insert(0, vals[1])
        self.txt_nombre.insert(0, vals[2])
        self.cbo_tipo.set(vals[3])
        self.cbo_estado.set(vals[4])

    # -------------------------------------------------------
    def limpiar(self):
        self.id_usuario = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)
        self.cbo_tipo.set("")
        self.cbo_estado.set("")

    # -------------------------------------------------------
    def guardar(self):
        dni = self.txt_dni.get().strip()
        nombre = self.txt_nombre.get().strip()
        tipo = self.cbo_tipo.get().strip()
        password = self.txt_password.get().strip()
        estado = self.cbo_estado.get().strip()

        # Validaciones
        if not dni.isdigit() or len(dni) != 8:
            messagebox.showwarning("Error", "El DNI debe tener 8 dígitos.")
            return

        if nombre == "" or password == "":
            messagebox.showwarning("Error", "Complete todos los campos.")
            return

        data = {
            "dni": dni,
            "nombre": nombre,
            "tipo": tipo,
            "password": password,
            "estado": estado,
        }

        if self.id_usuario is None:
            crear_usuario(data)
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
        else:
            actualizar_usuario(self.id_usuario, data)
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")

        self.cargar_tabla()
        self.limpiar()

    # -------------------------------------------------------
    def eliminar(self):
        if self.id_usuario is None:
            messagebox.showwarning("Aviso", "Seleccione un usuario.")
            return

        eliminar_usuario(self.id_usuario)
        messagebox.showinfo("Éxito", "Usuario eliminado.")

        self.cargar_tabla()
        self.limpiar()


# Test directo
if __name__ == "__main__":
    root = tk.Tk()
    app = UsuariosForm(master=root)
    app.mainloop()
