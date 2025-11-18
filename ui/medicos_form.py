# ui/medicos_form.py
# -----------------------------------------------------------
# Gestión de Médicos + Vista de Horarios del Médico Seleccionado
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

from models.medicos import listar_medicos, crear_medico, actualizar_medico, eliminar_medico
from models.horarios import listar_horarios


class MedicosForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Médicos")
        self.master.geometry("950x650")

        self.id_medico = None

        self.crear_widgets()
        self.cargar_tabla_medicos()

    # -----------------------------------------------------------
    def crear_widgets(self):

        # Título
        tk.Label(
            self.master,
            text="Gestión de Médicos",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # -------- FORMULARIO ---------
        form = tk.Frame(self.master)
        form.pack(pady=10)

        tk.Label(form, text="DNI:").grid(row=0, column=0, pady=5, sticky="e")
        tk.Label(form, text="Nombre:").grid(row=1, column=0, pady=5, sticky="e")
        tk.Label(form, text="Especialidad:").grid(row=2, column=0, pady=5, sticky="e")
        tk.Label(form, text="Estado:").grid(row=3, column=0, pady=5, sticky="e")

        self.txt_dni = tk.Entry(form, width=25)
        self.txt_nombre = tk.Entry(form, width=40)
        self.txt_especialidad = tk.Entry(form, width=40)
        self.cbo_estado = ttk.Combobox(form, values=["S", "N"], width=5)

        self.txt_dni.grid(row=0, column=1, padx=5)
        self.txt_nombre.grid(row=1, column=1, padx=5)
        self.txt_especialidad.grid(row=2, column=1, padx=5)
        self.cbo_estado.grid(row=3, column=1, padx=5)

        # -------- BOTONES ----------
        btns = tk.Frame(self.master)
        btns.pack(pady=10)

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar_form).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # -------- TABLA MÉDICOS ----------
        tk.Label(self.master, text="Lista de Médicos", font=("Segoe UI", 14, "bold")).pack(pady=5)

        self.tree_medicos = ttk.Treeview(
            self.master,
            columns=("ID", "DNI", "Nombre", "Especialidad", "Estado"),
            show="headings",
            height=8
        )

        headers = ["ID", "DNI", "Nombre", "Especialidad", "Estado"]
        widths = [60, 100, 200, 150, 80]

        for i, col in enumerate(headers):
            self.tree_medicos.heading(col, text=col)
            self.tree_medicos.column(col, width=widths[i])

        self.tree_medicos.pack(pady=10, fill="x")
        self.tree_medicos.bind("<<TreeviewSelect>>", self.seleccionar_medico)

        # -------- TABLA HORARIOS DEL MÉDICO ----------
        tk.Label(self.master, text="Horarios del Médico Seleccionado", font=("Segoe UI", 14, "bold")).pack(pady=5)

        self.tree_horarios = ttk.Treeview(
            self.master,
            columns=("ID", "Fecha", "Inicio", "Fin", "Disponible"),
            show="headings",
            height=8
        )

        headers2 = ["ID", "Fecha", "Inicio", "Fin", "Disponible"]
        widths2 = [60, 120, 100, 100, 100]

        for i, col in enumerate(headers2):
            self.tree_horarios.heading(col, text=col)
            self.tree_horarios.column(col, width=widths2[i])

        self.tree_horarios.pack(pady=5, fill="x")

    # ==========================================================
    #               CRUD MÉDICOS
    # ==========================================================
    def cargar_tabla_medicos(self):
        for item in self.tree_medicos.get_children():
            self.tree_medicos.delete(item)

        medicos = listar_medicos()

        for m in medicos:
            self.tree_medicos.insert("", tk.END, values=m)

    # -----------------------------------------------------------
    def seleccionar_medico(self, event):
        item = self.tree_medicos.selection()[0]
        vals = self.tree_medicos.item(item, "values")

        self.id_medico = vals[0]

        # Llenar formulario
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_especialidad.delete(0, tk.END)

        self.txt_dni.insert(0, vals[1])
        self.txt_nombre.insert(0, vals[2])
        self.txt_especialidad.insert(0, vals[3])
        self.cbo_estado.set(vals[4])

        # Cargar horarios del médico
        self.cargar_horarios_medico()

    # -----------------------------------------------------------
    def cargar_horarios_medico(self):
        """Carga horarios del médico seleccionado."""
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

        if not self.id_medico:
            return

        horarios = listar_horarios()

        # Filtrar por médico seleccionado
        for h in horarios:
            if str(h[1]).startswith(f"{self.id_medico} "):
                # Ignorar el nombre del médico y mostrar solo datos reales
                self.tree_horarios.insert("", tk.END, values=(
                    h[0],  # ID
                    h[2],  # Fecha
                    h[3],  # Inicio
                    h[4],  # Fin
                    h[5]   # Disponible
                ))

    # -----------------------------------------------------------
    def limpiar_form(self):
        self.id_medico = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_especialidad.delete(0, tk.END)
        self.cbo_estado.set("")

        # limpiar horarios
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

    # -----------------------------------------------------------
    def guardar(self):
        data = {
            "dni": self.txt_dni.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "especialidad": self.txt_especialidad.get().strip(),
            "estado": self.cbo_estado.get().strip()
        }

        if self.id_medico is None:
            crear_medico(data)
            messagebox.showinfo("Éxito", "Médico registrado.")
        else:
            actualizar_medico(self.id_medico, data)
            messagebox.showinfo("Éxito", "Datos actualizados.")

        self.cargar_tabla_medicos()
        self.limpiar_form()

    # -----------------------------------------------------------
    def eliminar(self):
        if self.id_medico is None:
            messagebox.showwarning("Aviso", "Seleccione un médico.")
            return

        eliminar_medico(self.id_medico)
        messagebox.showinfo("Éxito", "Médico eliminado.")

        self.cargar_tabla_medicos()
        self.limpiar_form()


# Para probar
if __name__ == "__main__":
    root = tk.Tk()
    app = MedicosForm(master=root)
    app.mainloop()

