# ui/citas_form.py
# -----------------------------------------------------------
# FORMULARIO CRUD PARA CITAS MÉDICAS – Versión Mejorada PRO
# -----------------------------------------------------------

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

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Citas Médicas")
        self.master.geometry("1100x700")

        self.id_cita_seleccionada = None

        self.crear_widgets()
        self.cargar_tabla()

    # -------------------------------------------------------
    def crear_widgets(self):

        tk.Label(self.master, text="Gestión de Citas Médicas",
                 font=("Segoe UI", 20, "bold")).pack(pady=10)

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
        self.cbo_medico.bind("<<ComboboxSelected>>", self.cargar_fechas)

        tk.Label(contenedor, text="Fecha disponible:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cbo_fecha = ttk.Combobox(contenedor, width=20, state="readonly")
        self.cbo_fecha.grid(row=2, column=1, sticky="w")
        self.cbo_fecha.bind("<<ComboboxSelected>>", self.cargar_horarios)

        tk.Label(contenedor, text="Horario:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cbo_horario = ttk.Combobox(contenedor, width=40, state="readonly")
        self.cbo_horario.grid(row=3, column=1)

        tk.Label(contenedor, text="Motivo:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.txt_motivo = tk.Entry(contenedor, width=40)
        self.txt_motivo.grid(row=4, column=1)

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
        columnas = ("ID", "Paciente", "Medico", "Especialidad", "Fecha", "Horario", "Motivo", "Registrado")

        self.tree = ttk.Treeview(
            self.master,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.pack(pady=10, fill="x")
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.cargar_pacientes()
        self.cargar_medicos()

    # -------------------------------------------------------
    def cargar_pacientes(self):
        pacientes = listar_pacientes()
        self.cbo_paciente["values"] = [f"{p[0]} - {p[2] if len(p)>2 else p[1]}" for p in pacientes]

    def cargar_medicos(self):
        medicos = listar_medicos()
        self.cbo_medico["values"] = [f"{m[0]} - {m[2]}" for m in medicos]

    # -------------------------------------------------------
    #        NUEVO: Cargar FECHAS dinámicamente
    # -------------------------------------------------------
    def cargar_fechas(self, event=None):
        medico_txt = self.cbo_medico.get()
        if not medico_txt:
            return

        id_medico = int(medico_txt.split(" - ")[0])

        fechas = listar_fechas_por_medico(id_medico)

        self.cbo_fecha["values"] = [f[0] for f in fechas]
        self.cbo_fecha.set("")
        self.cbo_horario.set("")

    # -------------------------------------------------------
    #      NUEVO: Cargar HORARIOS según la fecha elegida
    # -------------------------------------------------------
    def cargar_horarios(self, event=None):
        medico_txt = self.cbo_medico.get()
        fecha = self.cbo_fecha.get()

        if not medico_txt or not fecha:
            return

        id_medico = int(medico_txt.split(" - ")[0])

        horarios = listar_horarios_por_medico_y_fecha(id_medico, fecha)

        self.cbo_horario["values"] = [
            f"{h[0]} - {h[1]} a {h[2]}"
            for h in horarios
        ]
        self.cbo_horario.set("")

    # -------------------------------------------------------
    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        registros = listar_citas()
        for row in registros:
            self.tree.insert("", tk.END, values=row)

    # -------------------------------------------------------
    def limpiar_formulario(self):
        self.id_cita_seleccionada = None
        self.cbo_paciente.set("")
        self.cbo_medico.set("")
        self.cbo_fecha.set("")
        self.cbo_horario.set("")
        self.txt_motivo.delete(0, tk.END)

    # -------------------------------------------------------
    def seleccionar_fila(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.id_cita_seleccionada = valores[0]

    # -------------------------------------------------------
    def guardar(self):
        if self.cbo_paciente.get() == "" or self.cbo_medico.get() == "" or self.cbo_horario.get() == "":
            messagebox.showwarning("Aviso", "Complete todos los campos obligatorios.")
            return

        try:
            id_paciente = int(self.cbo_paciente.get().split(" - ")[0])
            id_horario = int(self.cbo_horario.get().split(" - ")[0])
        except:
            messagebox.showerror("Error", "Datos inválidos en los campos.")
            return

        data = {
            "id_paciente": id_paciente,
            "id_horario": id_horario,
            "id_medico": int(self.cbo_medico.get().split(" - ")[0]),
            "motivo": self.txt_motivo.get(),
        }

        if self.id_cita_seleccionada is None:
            crear_cita(data)
            messagebox.showinfo("Éxito", "Cita creada.")
        else:
            actualizar_cita(self.id_cita_seleccionada, data)
            messagebox.showinfo("Éxito", "Cita actualizada.")

        self.cargar_tabla()
        self.limpiar_formulario()

    # -------------------------------------------------------
    def eliminar(self):
        if self.id_cita_seleccionada is None:
            messagebox.showwarning("Aviso", "Seleccione una cita.")
            return

        eliminar_cita(self.id_cita_seleccionada)
        messagebox.showinfo("Éxito", "Cita eliminada.")

        self.cargar_tabla()
        self.limpiar_formulario()


# Para pruebas rápidas
if __name__ == "__main__":
    root = tk.Tk()
    app = CitasForm(master=root)
    root.mainloop()
