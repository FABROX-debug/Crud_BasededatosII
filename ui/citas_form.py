# ui/citas_form.py
# -----------------------------------------------------------
# FORMULARIO CRUD PARA CITA_MEDICA (Tkinter + ttk)
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from models.citas import listar_citas, crear_cita, actualizar_cita, eliminar_cita
from models.pacientes import listar_pacientes
from models.medicos import listar_medicos
from models.horarios import (
    listar_horarios_disponibles,
    listar_fechas_disponibles,
    obtener_horario_por_id,
)
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
        self.metadatos_citas = {}
        self.pacientes_cache = []
        self.medicos_cache = []
        self.horario_actual_edicion = None

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
        self.cbo_paciente = ttk.Combobox(contenedor, width=40, state="readonly")
        self.cbo_paciente.grid(row=0, column=1)

        tk.Label(contenedor, text="Médico:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cbo_medico = ttk.Combobox(contenedor, width=40, state="readonly")
        self.cbo_medico.grid(row=1, column=1)
        self.cbo_medico.bind("<<ComboboxSelected>>", self.on_medico_cambiado)

        tk.Label(contenedor, text="Fecha disponible:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cbo_fecha = ttk.Combobox(contenedor, width=18, state="readonly")
        self.cbo_fecha.grid(row=2, column=1, sticky="w")
        self.cbo_fecha.bind("<<ComboboxSelected>>", self.actualizar_horarios)
        tk.Button(contenedor, text="Ver fechas", width=14,
                  command=self.cargar_fechas_para_medico).grid(row=2, column=2, padx=5)

        tk.Label(contenedor, text="Horario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cbo_horario = ttk.Combobox(contenedor, width=40, state="readonly")
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
        self.metadatos_citas = {}
        for row in registros:
            if len(row) >= 10:
                self.metadatos_citas[row[0]] = {
                    "id_paciente": row[7],
                    "id_medico": row[8],
                    "id_horario": row[9],
                }
            self.tree.insert("", tk.END, values=row[:7])

    # -------------------------------------------------------
    def cargar_pacientes(self):
        self.pacientes_cache = listar_pacientes()
        self.cbo_paciente["values"] = [f"{p[0]} - {p[1]} (DNI: {p[2]})" for p in self.pacientes_cache]

    # -------------------------------------------------------
    def cargar_medicos(self):
        self.medicos_cache = listar_medicos()
        self.cbo_medico["values"] = [f"{m[0]} - {m[1]} ({m[3]})" for m in self.medicos_cache]

    # -------------------------------------------------------
    def on_medico_cambiado(self, event=None):
        """Cuando cambia el médico, refrescamos fechas y horarios."""
        self.cbo_fecha.set("")
        self.cbo_horario.set("")
        self.horarios_cache = []
        if not self.id_cita_seleccionada:
            self.horario_actual_edicion = None
        self.cargar_fechas_para_medico()

    # -------------------------------------------------------
    def cargar_fechas_para_medico(self, horario_actual=None):
        medico_id = self._extraer_id_desde_combo(self.cbo_medico.get())
        if medico_id is None:
            return

        fechas = listar_fechas_disponibles(medico_id, horario_actual or self.horario_actual_edicion)
        self.cbo_fecha["values"] = fechas

        if fechas:
            fecha_seleccion = None
            if self.horario_actual_edicion:
                actual = obtener_horario_por_id(self.horario_actual_edicion)
                if actual:
                    fecha_seleccion = actual[2]
            if fecha_seleccion and fecha_seleccion in fechas:
                self.cbo_fecha.set(fecha_seleccion)
            else:
                self.cbo_fecha.current(0)
            self.actualizar_horarios()
        else:
            messagebox.showinfo(
                "Sin fechas",
                "El médico seleccionado no tiene fechas disponibles.",
            )

    # -------------------------------------------------------
    def actualizar_horarios(self, event=None, horario_actual=None):
        medico_id = self._extraer_id_desde_combo(self.cbo_medico.get())
        fecha = self.cbo_fecha.get().strip()

        if medico_id is None or fecha == "":
            return

        if not es_fecha_valida(fecha):
            messagebox.showwarning("Fecha inválida", "Seleccione una fecha válida (YYYY-MM-DD).")
            return

        horario_ref = horario_actual or self.horario_actual_edicion
        self.horarios_cache = listar_horarios_disponibles(medico_id, fecha, horario_ref)
        opciones = [self._formatear_horario(h) for h in self.horarios_cache]

        self.cbo_horario["values"] = opciones
        self.cbo_horario.set("")

        if opciones:
            if horario_ref:
                for idx, h in enumerate(self.horarios_cache):
                    if h[0] == horario_ref:
                        self.cbo_horario.current(idx)
                        break
                else:
                    self.cbo_horario.current(0)
            else:
                self.cbo_horario.current(0)
            self.establecer_fecha_desde_horario()
        else:
            messagebox.showinfo(
                "Sin horarios",
                "No hay horarios disponibles para esa fecha.",
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
                if self.cbo_fecha.get() != h[1]:
                    self.cbo_fecha.set(h[1])
                break

    # -------------------------------------------------------
    def limpiar_formulario(self):
        self.id_cita_seleccionada = None
        self.horario_actual_edicion = None
        self.cbo_paciente.set("")
        self.cbo_medico.set("")
        self.cbo_fecha.set("")
        self.cbo_horario.set("")
        self.txt_motivo.delete(0, tk.END)
        self.horarios_cache = []

    # -------------------------------------------------------
    def seleccionar_fila(self, event):
        if not self.tree.selection():
            return

        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.id_cita_seleccionada = valores[0]

        meta = self.metadatos_citas.get(self.id_cita_seleccionada, {})
        self.horario_actual_edicion = meta.get("id_horario")

        self._seleccionar_combo_por_id(self.cbo_paciente, meta.get("id_paciente"))
        self._seleccionar_combo_por_id(self.cbo_medico, meta.get("id_medico"))

        self.cbo_fecha.set(valores[4])
        self.cargar_fechas_para_medico()
        self.actualizar_horarios(horario_actual=self.horario_actual_edicion)
        self.cbo_horario.set(valores[5])

        self.txt_motivo.delete(0, tk.END)
        self.txt_motivo.insert(0, valores[6])

    # -------------------------------------------------------
    def guardar(self):
        from tkinter import messagebox

        fecha = self.cbo_fecha.get().strip()
        if not es_fecha_valida(fecha):
            messagebox.showwarning("Fecha inválida", "Ingrese una fecha válida en formato YYYY-MM-DD.")
            return

        if self.cbo_paciente.get() == "" or self.cbo_medico.get() == "" or self.cbo_horario.get() == "":
            messagebox.showwarning("Aviso", "Seleccione paciente, médico y horario.")
            return

        try:
            id_paciente = self._extraer_id_desde_combo(self.cbo_paciente.get())
            id_horario = self._extraer_id_desde_combo(self.cbo_horario.get())
            id_medico = self._extraer_id_desde_combo(self.cbo_medico.get())
        except Exception:
            messagebox.showerror("Error", "Paciente, médico u horario no válidos.")
            return

        if id_paciente is None or id_medico is None or id_horario is None:
            messagebox.showerror("Error", "Seleccione opciones válidas para la cita.")
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
    def _seleccionar_combo_por_id(self, combo, id_buscar):
        if id_buscar is None:
            return
        for opcion in combo["values"]:
            try:
                if int(opcion.split(" - ")[0]) == int(id_buscar):
                    combo.set(opcion)
                    return
            except ValueError:
                continue

    def _extraer_id_desde_combo(self, texto):
        if texto == "":
            return None
        try:
            return int(texto.split(" - ")[0])
        except (ValueError, IndexError):
            return None

    def _formatear_horario(self, horario_tuple):
        horario_id, fecha, inicio, fin = horario_tuple[:4]
        return f"{horario_id} - {fecha} | {inicio} a {fin}"
