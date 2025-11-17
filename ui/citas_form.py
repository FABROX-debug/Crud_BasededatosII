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


class CitasForm(tk.Frame):

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Citas Médicas")
        self.master.geometry("1050x650")

        self.id_cita_seleccionada = None

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

        tk.Label(contenedor, text="Fecha: (YYYY-MM-DD)").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.txt_fecha = tk.Entry(contenedor, width=20)
        self.txt_fecha.grid(row=2, column=1, sticky="w")

        tk.Label(contenedor, text="Horario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cbo_horario = ttk.Combobox(contenedor, width=40)
        self.cbo_horario.grid(row=3, column=1)

        tk.Label(contenedor, text="Motivo:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.txt_motivo = tk.Entry(contenedor, width=40)
        self.txt_motivo.grid(row=4, column=1)

        tk.Label(contenedor, text="Estado Cita:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.cbo_estado = ttk.Combobox(contenedor, values=["PENDIENTE", "CONFIRMADA", "CANCELADA"], width=20)
        self.cbo_estado.grid(row=5, column=1, sticky="w")

        tk.Label(contenedor, text="Estado Pago:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.cbo_pago = ttk.Combobox(contenedor, values=["PENDIENTE", "PAGADO"], width=20)
        self.cbo_pago.grid(row=6, column=1, sticky="w")

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
            columns=("ID", "Paciente", "Médico", "Especialidad", "Fecha", "Hora", "Estado", "Pago"),
            show="headings",
            height=15
        )
        headers = ["ID", "Paciente", "Médico", "Especialidad", "Fecha", "Hora", "Estado Cita", "Estado Pago"]
        for i, col in enumerate(headers):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=130)

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
        self.cbo_paciente["values"] = [f"{p[0]} - {p[1]}" for p in pacientes]

    # -------------------------------------------------------
    def cargar_medicos(self):
        medicos = listar_medicos()
        self.cbo_medico["values"] = [f"{m[0]} - {m[1]}" for m in medicos]

    # -------------------------------------------------------
    def actualizar_horarios(self, event=None):
        medico_txt = self.cbo_medico.get()
        if medico_txt == "":
            return
        id_medico = int(medico_txt.split(" - ")[0])
        fecha = self.txt_fecha.get()

        if fecha == "":
            messagebox.showwarning("Aviso", "Ingrese la fecha antes de elegir el horario.")
            return

        horarios = listar_horarios_disponibles(id_medico, fecha)
        self.cbo_horario["values"] = [f"{h[0]} - {h[1]} a {h[2]}" for h in horarios]

    # -------------------------------------------------------
    def limpiar_formulario(self):
        self.id_cita_seleccionada = None
        self.cbo_paciente.set("")
        self.cbo_medico.set("")
        self.txt_fecha.delete(0, tk.END)
        self.cbo_horario.set("")
        self.txt_motivo.delete(0, tk.END)
        self.cbo_estado.set("")
        self.cbo_pago.set("")

    # -------------------------------------------------------
    def seleccionar_fila(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.id_cita_seleccionada = valores[0]

    # -------------------------------------------------------
    def guardar(self):

        if self.id_cita_seleccionada is None:
            # INSERTAR
            try:
                id_paciente = int(self.cbo_paciente.get().split(" - ")[0])
                id_horario = int(self.cbo_horario.get().split(" - ")[0])

                data = {
                    "id_paciente": id_paciente,
                    "id_horario": id_horario,
                    "estado_cita": self.cbo_estado.get(),
                    "estado_pago": self.cbo_pago.get(),
                    "motivo": self.txt_motivo.get(),
                    "observaciones": "",
                }

                crear_cita(data)
                messagebox.showinfo("Éxito", "Cita creada correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la cita:\n{e}")

        else:
            # ACTUALIZAR
            try:
                id_paciente = int(self.cbo_paciente.get().split(" - ")[0])
                id_horario = int(self.cbo_horario.get().split(" - ")[0])

                data = {
                    "id_paciente": id_paciente,
                    "id_horario": id_horario,
                    "estado_cita": self.cbo_estado.get(),
                    "estado_pago": self.cbo_pago.get(),
                    "motivo": self.txt_motivo.get(),
                    "observaciones": "",
                }

                actualizar_cita(self.id_cita_seleccionada, data)
                messagebox.showinfo("Éxito", "Cita actualizada correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la cita:\n{e}")

        self.cargar_tabla()
        self.limpiar_formulario()

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
