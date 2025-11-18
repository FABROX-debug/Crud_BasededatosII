# ui/medicos_form.py - VERSIÓN CORREGIDA
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

    def crear_widgets(self):
        # Título
        tk.Label(
            self.master,
            text="Gestión de Médicos",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # FORMULARIO
        form = tk.Frame(self.master)
        form.pack(pady=10)

        tk.Label(form, text="DNI:").grid(row=0, column=0, pady=5, sticky="e", padx=5)
        tk.Label(form, text="Nombre:").grid(row=1, column=0, pady=5, sticky="e", padx=5)
        tk.Label(form, text="Especialidad:").grid(row=2, column=0, pady=5, sticky="e", padx=5)
        tk.Label(form, text="Estado:").grid(row=3, column=0, pady=5, sticky="e", padx=5)

        self.txt_dni = tk.Entry(form, width=25)
        self.txt_nombre = tk.Entry(form, width=40)
        self.txt_especialidad = tk.Entry(form, width=40)
        self.cbo_estado = ttk.Combobox(form, values=["S", "N"], width=5, state="readonly")

        self.txt_dni.grid(row=0, column=1, padx=5)
        self.txt_nombre.grid(row=1, column=1, padx=5)
        self.txt_especialidad.grid(row=2, column=1, padx=5)
        self.cbo_estado.grid(row=3, column=1, padx=5)

        # BOTONES
        btns = tk.Frame(self.master)
        btns.pack(pady=10)

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar_form).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # TABLA MÉDICOS
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

        # TABLA HORARIOS DEL MÉDICO
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

    def cargar_tabla_medicos(self):
        for item in self.tree_medicos.get_children():
            self.tree_medicos.delete(item)

        try:
            medicos = listar_medicos()
            for m in medicos:
                self.tree_medicos.insert("", tk.END, values=m)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos:\n{e}")

    def seleccionar_medico(self, event):
        try:
            item = self.tree_medicos.selection()[0]
            vals = self.tree_medicos.item(item, "values")
        except:
            return

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

    def cargar_horarios_medico(self):
        """Carga horarios del médico seleccionado - VERSIÓN CORREGIDA"""
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

        if not self.id_medico:
            return

        try:
            # Obtener TODOS los horarios
            todos_horarios = listar_horarios()

            # Filtrar por ID del médico seleccionado
            for h in todos_horarios:
                # h = (ID_HORARIO, MEDICO_NOMBRE, FECHA, HORA_INICIO, HORA_FIN, DISPONIBLE)
                # Extraer ID del médico del campo "MEDICO_NOMBRE" (formato: "ID - Nombre")
                medico_info = h[1]  # "ID - Nombre (Especialidad)"

                try:
                    id_medico_horario = int(medico_info.split(" - ")[0])

                    # Solo mostrar si coincide con el médico seleccionado
                    if id_medico_horario == int(self.id_medico):
                        self.tree_horarios.insert("", tk.END, values=(
                            h[0],  # ID_HORARIO
                            h[2],  # Fecha
                            h[3],  # Hora inicio
                            h[4],  # Hora fin
                            h[5]  # Disponible
                        ))
                except (ValueError, IndexError):
                    continue

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar horarios:\n{e}")

    def limpiar_form(self):
        self.id_medico = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_especialidad.delete(0, tk.END)
        self.cbo_estado.set("")

        # Limpiar horarios
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

    def validar_datos(self):
        """Valida los datos del formulario"""
        dni = self.txt_dni.get().strip()
        nombre = self.txt_nombre.get().strip()
        especialidad = self.txt_especialidad.get().strip()
        estado = self.cbo_estado.get()

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showwarning("Error", "El DNI debe tener 8 dígitos.")
            return False

        if nombre == "" or len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener al menos 3 caracteres.")
            return False

        if especialidad == "" or len(especialidad) < 3:
            messagebox.showwarning("Error", "La especialidad debe tener al menos 3 caracteres.")
            return False

        if estado not in ["S", "N"]:
            messagebox.showwarning("Error", "Debe seleccionar un estado válido (S/N).")
            return False

        return True

    def guardar(self):
        if not self.validar_datos():
            return

        data = {
            "dni": self.txt_dni.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "especialidad": self.txt_especialidad.get().strip(),
            "estado": self.cbo_estado.get().strip()
        }

        try:
            if self.id_medico is None:
                crear_medico(data)
                messagebox.showinfo("Éxito", "Médico registrado correctamente.")
            else:
                actualizar_medico(self.id_medico, data)
                messagebox.showinfo("Éxito", "Médico actualizado correctamente.")

            self.cargar_tabla_medicos()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def eliminar(self):
        if self.id_medico is None:
            messagebox.showwarning("Aviso", "Seleccione un médico.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar este médico?\nEsta acción no se puede deshacer."
        )

        if not respuesta:
            return

        try:
            eliminar_medico(self.id_medico)
            messagebox.showinfo("Éxito", "Médico eliminado correctamente.")
            self.cargar_tabla_medicos()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicosForm(master=root)
    app.mainloop()
