# ui/citas_form.py
# -----------------------------------------------------------
# FORMULARIO CRUD PARA CITA_MEDICA (Tkinter + ttk)
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from models.citas import listar_citas, crear_cita, actualizar_cita, eliminar_cita
from models.pacientes import listar_pacientes
from models.medicos import listar_medicos
from models.horarios import listar_horarios_disponibles
from utils.validators import es_fecha_valida


class CitasForm(tk.Frame):

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Citas Médicas")
        self.master.geometry("1050x650")

        self.id_cita_seleccionada = None
        self.horarios_cache = []

        self.crear_widgets()
        self.cargar_tabla()

    # -------------------------------------------------------
    def crear_widgets(self):

        tk.Label(self.master, text="Gestión de Citas Médicas",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        contenedor = tk.Frame(self.master)
        contenedor.pack(pady=10)

        # -----------------------------
        # CAMPOS DEL FORMULARIO
        # -----------------------------
        tk.Label(contenedor, text="Paciente:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.cbo_paciente = ttk.Combobox(contenedor, width=40)
        self.cbo_paciente.grid(row=0, column=1)

        tk.Label(contenedor, text="Médico:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cbo_medico = ttk.Combobox(contenedor, width=40)
        self.cbo_medico.grid(row=1, column=1)
        self.cbo_medico.bind("<<ComboboxSelected>>", self.actualizar_horarios)

        tk.Label(contenedor, text="Fecha disponible:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.txt_fecha = tk.Entry(contenedor, width=20, state="readonly")
        self.txt_fecha.grid(row=2, column=1, sticky="w")

        tk.Label(contenedor, text="Horario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cbo_horario = ttk.Combobox(contenedor, width=40)
        self.cbo_horario.grid(row=3, column=1)
        self.cbo_horario.bind("<<ComboboxSelected>>", self.establecer_fecha_desde_horario)

        tk.Label(contenedor, text="Motivo/Observaciones:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.txt_motivo = tk.Entry(contenedor, width=60)
        self.txt_motivo.grid(row=4, column=1, sticky="w", pady=5)
        # -----------------------------
        # BOTONES
        # -----------------------------
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Nuevo", width=12, command=self.limpiar_formulario).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # -----------------------------
        # TABLA
        # -----------------------------
        self.tree = ttk.Treeview(
            self.master,
            columns=("ID", "Paciente", "Médico", "Especialidad", "Fecha", "Horario", "Motivo"),
            show="headings",
            height=15
        )
        headers = ["ID", "Paciente", "Médico", "Especialidad", "Fecha", "Horario", "Motivo"]
        widths = [60, 180, 180, 150, 100, 160, 200]
        for i, col in enumerate(headers):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=widths[i])

        self.tree.pack(pady=10, fill="x")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_pacientes()
        self.cargar_medicos()

    # -------------------------------------------------------
    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        registros = listar_citas()
        for row in registros:
            self.tree.insert("", tk.END, values=row)

    # -------------------------------------------------------
    def cargar_pacientes(self):
        pacientes = listar_pacientes()
        self.cbo_paciente["values"] = [f"{p[0]} - {p[1]} (DNI: {p[2]})" for p in pacientes]

    # -------------------------------------------------------
    def cargar_medicos(self):
        medicos = listar_medicos()
        self.cbo_medico["values"] = [f"{m[0]} - {m[1]} ({m[3]})" for m in medicos]

    # -------------------------------------------------------
    def actualizar_horarios(self, event=None):
        medico_txt = self.cbo_medico.get()
        if medico_txt == "":
            return

        id_medico = int(medico_txt.split(" - ")[0])

        # Si hay una fecha ingresada úsala, de lo contrario trae todas las futuras
        fecha = self.txt_fecha.get().strip()
        if not fecha:
            from datetime import date
            fecha = date.today().strftime("%Y-%m-%d")

        if not es_fecha_valida(fecha):
            from tkinter import messagebox
            messagebox.showwarning("Fecha inválida", "Ingrese una fecha válida en formato YYYY-MM-DD.")
            return

        self.horarios_cache = listar_horarios_disponibles(id_medico, fecha)
        opciones = [f"{h[0]} - {h[1]} | {h[2]} a {h[3]}" for h in self.horarios_cache]
        self.cbo_horario["values"] = opciones
        self.cbo_horario.set("")
        if opciones:
            self.cbo_horario.current(0)
            self.establecer_fecha_desde_horario()
        else:
            messagebox.showinfo(
                "Sin horarios",
                "El médico seleccionado no tiene horarios disponibles para la fecha indicada."
            )

    # -------------------------------------------------------
    def establecer_fecha_desde_horario(self, event=None):
        if not self.cbo_horario.get() or not self.horarios_cache:
            return

        try:
            horario_id = int(self.cbo_horario.get().split(" - ")[0])
        except ValueError:
            return

        for h in self.horarios_cache:
            if h[0] == horario_id:
                self.txt_fecha.config(state="normal")
                self.txt_fecha.delete(0, tk.END)
                self.txt_fecha.insert(0, h[1])
                self.txt_fecha.config(state="readonly")
                break

    # -------------------------------------------------------
    def limpiar_formulario(self):
        self.id_cita_seleccionada = None
        self.cbo_paciente.set("")
        self.cbo_medico.set("")
        self.txt_fecha.config(state="normal")
        self.txt_fecha.delete(0, tk.END)
        self.txt_fecha.config(state="readonly")
        self.cbo_horario.set("")
        self.txt_motivo.delete(0, tk.END)
        self.horarios_cache = []

    # -------------------------------------------------------
    def seleccionar_fila(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.id_cita_seleccionada = valores[0]
        paciente_nombre, medico_nombre = valores[1], valores[2]

        self._seleccionar_combo_por_nombre(self.cbo_paciente, paciente_nombre)
        self._seleccionar_combo_por_nombre(self.cbo_medico, medico_nombre)

        self.txt_fecha.config(state="normal")
        self.txt_fecha.delete(0, tk.END)
        self.txt_fecha.insert(0, valores[4])
        self.txt_fecha.config(state="readonly")

        self.cbo_horario.set(valores[5])
        self.txt_motivo.delete(0, tk.END)
        self.txt_motivo.insert(0, valores[6])

    # -------------------------------------------------------
    def guardar(self):
        from tkinter import messagebox

        fecha = self.txt_fecha.get().strip()
        if not es_fecha_valida(fecha):
            messagebox.showwarning("Fecha inválida", "Ingrese una fecha válida en formato YYYY-MM-DD.")
            return

        if self.cbo_paciente.get() == "" or self.cbo_medico.get() == "" or self.cbo_horario.get() == "":
            messagebox.showwarning("Aviso", "Seleccione paciente, médico y horario.")
            return

        try:
            id_paciente = int(self.cbo_paciente.get().split(" - ")[0])
            id_horario = int(self.cbo_horario.get().split(" - ")[0])
            id_medico = int(self.cbo_medico.get().split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Paciente, médico u horario no válidos.")
            return

        data = {
            "id_paciente": id_paciente,
            "id_medico": id_medico,
            "id_horario": id_horario,
            "motivo": self.txt_motivo.get(),
        }

        try:
            if self.id_cita_seleccionada is None:
                # INSERTAR
                crear_cita(data)
                messagebox.showinfo("Éxito", "Cita creada correctamente.")
            else:
                # ACTUALIZAR
                actualizar_cita(self.id_cita_seleccionada, data)
                messagebox.showinfo("Éxito", "Cita actualizada correctamente.")

            self.cargar_tabla()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la cita:\n{e}")

    # -------------------------------------------------------
    def eliminar(self):
        if self.id_cita_seleccionada is None:
            messagebox.showwarning("Aviso", "Seleccione una cita para eliminar.")
            return

        try:
            eliminar_cita(self.id_cita_seleccionada)
            messagebox.showinfo("Éxito", "Cita eliminada correctamente.")
            self.cargar_tabla()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la cita:\n{e}")

    # -------------------------------------------------------
    def _seleccionar_combo_por_nombre(self, combo, nombre_objetivo):
        for opcion in combo["values"]:
            if nombre_objetivo in opcion:
                combo.set(opcion)
                return
