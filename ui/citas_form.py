# ui/citas_form.py - VERSIÓN CORREGIDA
import tkinter as tk
from tkinter import ttk, messagebox

from models.citas import listar_citas, crear_cita, actualizar_cita, eliminar_cita
from models.pacientes import listar_pacientes
from models.medicos import listar_medicos
from models.horarios import (
    listar_fechas_por_medico,
    listar_horarios_por_medico_y_fecha
)


class CitasForm(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Citas Médicas")
        self.master.geometry("1150x700")

        self.id_cita_seleccionada = None

        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        tk.Label(self.master, text="Gestión de Citas Médicas",
                 font=("Segoe UI", 20, "bold")).pack(pady=10)

        contenedor = tk.Frame(self.master)
        contenedor.pack(pady=10)

        # CAMPOS DEL FORMULARIO
        tk.Label(contenedor, text="Paciente:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.cbo_paciente = ttk.Combobox(contenedor, width=40, state="readonly")
        self.cbo_paciente.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(contenedor, text="Médico:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cbo_medico = ttk.Combobox(contenedor, width=40, state="readonly")
        self.cbo_medico.grid(row=1, column=1, sticky="w", padx=5)
        self.cbo_medico.bind("<<ComboboxSelected>>", self.cargar_fechas)

        tk.Label(contenedor, text="Fecha disponible:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cbo_fecha = ttk.Combobox(contenedor, width=20, state="readonly")
        self.cbo_fecha.grid(row=2, column=1, sticky="w", padx=5)
        self.cbo_fecha.bind("<<ComboboxSelected>>", self.cargar_horarios)

        tk.Label(contenedor, text="Horario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cbo_horario = ttk.Combobox(contenedor, width=40, state="readonly")
        self.cbo_horario.grid(row=3, column=1, sticky="w", padx=5)

        tk.Label(contenedor, text="Motivo:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.txt_motivo = tk.Entry(contenedor, width=43)
        self.txt_motivo.grid(row=4, column=1, sticky="w", padx=5)

        # BOTONES
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Nuevo", width=12, command=self.limpiar_formulario).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Actualizar Tabla", width=12, command=self.cargar_tabla).grid(row=0, column=3, padx=5)

        # TABLA
        columnas = ("ID", "Paciente", "Medico", "Especialidad", "Fecha", "Horario", "Motivo", "Registrado")

        self.tree = ttk.Treeview(
            self.master,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50)
        self.tree.column("Paciente", width=150)
        self.tree.column("Medico", width=150)
        self.tree.column("Especialidad", width=120)
        self.tree.column("Fecha", width=100)
        self.tree.column("Horario", width=120)
        self.tree.column("Motivo", width=180)
        self.tree.column("Registrado", width=130)

        self.tree.pack(pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_pacientes()
        self.cargar_medicos()

    def cargar_pacientes(self):
        """Carga lista de pacientes"""
        try:
            pacientes = listar_pacientes()
            self.cbo_paciente["values"] = [
                f"{p[0]} - {p[2]}" for p in pacientes
            ]
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes:\n{e}")

    def cargar_medicos(self):
        """Carga lista de médicos activos"""
        try:
            medicos = listar_medicos()
            # Filtrar solo médicos activos
            medicos_activos = [m for m in medicos if m[4] == "S"]
            self.cbo_medico["values"] = [
                f"{m[0]} - {m[2]} ({m[3]})" for m in medicos_activos
            ]
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos:\n{e}")

    def cargar_fechas(self, event=None):
        """Carga fechas disponibles según médico seleccionado"""
        medico_txt = self.cbo_medico.get()
        if not medico_txt:
            return

        try:
            id_medico = int(medico_txt.split(" - ")[0])
            fechas = listar_fechas_por_medico(id_medico)

            if len(fechas) == 0:
                messagebox.showinfo(
                    "Sin fechas",
                    "Este médico no tiene fechas disponibles.\nPor favor, registre horarios primero."
                )
                self.cbo_fecha["values"] = []
                self.cbo_fecha.set("")
                self.cbo_horario["values"] = []
                self.cbo_horario.set("")
                return

            self.cbo_fecha["values"] = [f[0] for f in fechas]
            self.cbo_fecha.set("")
            self.cbo_horario.set("")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar fechas:\n{e}")

    def cargar_horarios(self, event=None):
        """Carga horarios disponibles según médico y fecha"""
        medico_txt = self.cbo_medico.get()
        fecha = self.cbo_fecha.get()

        if not medico_txt or not fecha:
            return

        try:
            id_medico = int(medico_txt.split(" - ")[0])
            horarios = listar_horarios_por_medico_y_fecha(id_medico, fecha)

            if len(horarios) == 0:
                messagebox.showinfo(
                    "Sin horarios",
                    "No hay horarios disponibles para esta fecha."
                )
                self.cbo_horario["values"] = []
                self.cbo_horario.set("")
                return

            self.cbo_horario["values"] = [
                f"{h[0]} - {h[1]} a {h[2]}" for h in horarios
            ]
            self.cbo_horario.set("")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar horarios:\n{e}")

    def cargar_tabla(self):
        """Recarga la tabla de citas"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            registros = listar_citas()
            for row in registros:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar citas:\n{e}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.id_cita_seleccionada = None
        self.cbo_paciente.set("")
        self.cbo_medico.set("")
        self.cbo_fecha.set("")
        self.cbo_fecha["values"] = []
        self.cbo_horario.set("")
        self.cbo_horario["values"] = []
        self.txt_motivo.delete(0, tk.END)

    def seleccionar_fila(self, event):
        """Selecciona una fila de la tabla"""
        try:
            item = self.tree.selection()[0]
            valores = self.tree.item(item, "values")
            self.id_cita_seleccionada = valores[0]
        except:
            pass

    def validar_formulario(self):
        """Valida que todos los campos estén completos"""
        if self.cbo_paciente.get() == "":
            messagebox.showwarning("Campo requerido", "Debe seleccionar un paciente.")
            return False

        if self.cbo_medico.get() == "":
            messagebox.showwarning("Campo requerido", "Debe seleccionar un médico.")
            return False

        if self.cbo_fecha.get() == "":
            messagebox.showwarning("Campo requerido", "Debe seleccionar una fecha.")
            return False

        if self.cbo_horario.get() == "":
            messagebox.showwarning("Campo requerido", "Debe seleccionar un horario.")
            return False

        return True

    def guardar(self):
        """Guarda o actualiza una cita"""
        if not self.validar_formulario():
            return

        try:
            id_paciente = int(self.cbo_paciente.get().split(" - ")[0])
            id_medico = int(self.cbo_medico.get().split(" - ")[0])
            id_horario = int(self.cbo_horario.get().split(" - ")[0])
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos en los campos.")
            return

        data = {
            "id_paciente": id_paciente,
            "id_medico": id_medico,
            "id_horario": id_horario,
            "motivo": self.txt_motivo.get().strip(),
        }

        try:
            if self.id_cita_seleccionada is None:
                crear_cita(data)
                messagebox.showinfo("Éxito", "Cita creada correctamente.")
            else:
                actualizar_cita(self.id_cita_seleccionada, data)
                messagebox.showinfo("Éxito", "Cita actualizada correctamente.")

            self.cargar_tabla()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la cita:\n{e}")

    def eliminar(self):
        """Elimina una cita seleccionada"""
        if self.id_cita_seleccionada is None:
            messagebox.showwarning("Aviso", "Debe seleccionar una cita para eliminar.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar esta cita?\nEl horario quedará disponible nuevamente."
        )

        if not respuesta:
            return

        try:
            eliminar_cita(self.id_cita_seleccionada)
            messagebox.showinfo("Éxito", "Cita eliminada correctamente.")
            self.cargar_tabla()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la cita:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CitasForm(master=root)
    root.mainloop()