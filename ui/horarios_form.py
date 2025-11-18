# ui/horarios_form.py
# -----------------------------------------------------------
# CRONOGRAMA DE HORARIOS MÉDICOS (Optimizado)
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

from models.horarios import listar_horarios, crear_horario, actualizar_horario, eliminar_horario
from models.medicos import listar_medicos

from utils.validators import es_fecha_valida
import re


class HorariosForm(tk.Frame):

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Horarios Médicos")
        self.master.geometry("800x600")

        self.id_horario = None

        self.crear_widgets()
        self.cargar_medicos()
        self.cargar_tabla()

    # -------------------------------------------------------
    def crear_widgets(self):

        tk.Label(self.master, text="Gestión de Horarios Médicos",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        frm = tk.Frame(self.master)
        frm.pack(pady=10)

        # Labels
        labels = [
            "Médico:",
            "Fecha (YYYY-MM-DD):",
            "Hora inicio (HH:MM):",
            "Hora fin (HH:MM):",
            "Disponible:"
        ]

        for i, text in enumerate(labels):
            tk.Label(frm, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)

        # Campos
        self.cbo_medico = ttk.Combobox(frm, width=35, state="readonly")
        self.txt_fecha = tk.Entry(frm, width=20)
        self.txt_hora_inicio = tk.Entry(frm, width=20)
        self.txt_hora_fin = tk.Entry(frm, width=20)
        self.cbo_disponible = ttk.Combobox(frm, values=["S", "N"], width=5, state="readonly")

        self.cbo_medico.grid(row=0, column=1)
        self.txt_fecha.grid(row=1, column=1)
        self.txt_hora_inicio.grid(row=2, column=1)
        self.txt_hora_fin.grid(row=3, column=1)
        self.cbo_disponible.grid(row=4, column=1)

        # Botones
        btns = tk.Frame(self.master)
        btns.pack(pady=10)

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar_form).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # Tabla
        self.tree = ttk.Treeview(
            self.master,
            columns=("ID", "Médico", "Fecha", "Inicio", "Fin", "Disp"),
            show="headings",
            height=14
        )

        headers = ["ID", "Médico", "Fecha", "Inicio", "Fin", "Disponible"]
        for i, h in enumerate(headers):
            self.tree.heading(i, text=h)

        self.tree.column(0, width=60)
        self.tree.column(1, width=180)
        self.tree.column(2, width=100)
        self.tree.column(3, width=80)
        self.tree.column(4, width=80)
        self.tree.column(5, width=80)

        self.tree.pack(fill="both", pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    # -------------------------------------------------------
    def cargar_medicos(self):
        medicos = listar_medicos()
        self.cbo_medico["values"] = [
            f"{m[0]} - {m[2]} ({m[3]})" for m in medicos
        ]

    # -------------------------------------------------------
    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for h in listar_horarios():
            self.tree.insert("", tk.END, values=h)

    # -------------------------------------------------------
    def seleccionar(self, event):
        try:
            item = self.tree.selection()[0]
            vals = self.tree.item(item, "values")
        except:
            return

        self.id_horario = vals[0]

        self.cbo_medico.set(vals[1])
        self.txt_fecha.delete(0, tk.END)
        self.txt_hora_inicio.delete(0, tk.END)
        self.txt_hora_fin.delete(0, tk.END)
        self.cbo_disponible.set(vals[5])

        self.txt_fecha.insert(0, vals[2])
        self.txt_hora_inicio.insert(0, vals[3])
        self.txt_hora_fin.insert(0, vals[4])

    # -------------------------------------------------------
    def limpiar_form(self):
        self.id_horario = None
        self.cbo_medico.set("")
        self.txt_fecha.delete(0, tk.END)
        self.txt_hora_inicio.delete(0, tk.END)
        self.txt_hora_fin.delete(0, tk.END)
        self.cbo_disponible.set("")

    # -------------------------------------------------------
    def validar_hora(self, hora):
        """Valida formato HH:MM usando regex."""
        return bool(re.match(r"^[0-2][0-9]:[0-5][0-9]$", hora))

    # -------------------------------------------------------
    def guardar(self):

        # VALIDAR MÉDICO
        try:
            medico_id = int(self.cbo_medico.get().split(" - ")[0])
        except:
            messagebox.showerror("Error", "Seleccione un médico válido.")
            return

        # VALIDAR FECHA
        fecha = self.txt_fecha.get().strip()
        if not es_fecha_valida(fecha):
            messagebox.showwarning("Fecha inválida", "Ingrese fecha en formato YYYY-MM-DD.")
            return

        # VALIDAR HORAS
        h_inicio = self.txt_hora_inicio.get().strip()
        h_fin = self.txt_hora_fin.get().strip()

        if not self.validar_hora(h_inicio) or not self.validar_hora(h_fin):
            messagebox.showerror("Error", "Las horas deben ser formato HH:MM")
            return

        if h_inicio >= h_fin:
            messagebox.showerror("Error", "La hora de inicio debe ser menor a la hora fin.")
            return

        data = {
            "id_medico": medico_id,
            "fecha": fecha,
            "hora_inicio": h_inicio,
            "hora_fin": h_fin,
            "disponible": self.cbo_disponible.get() or "S"
        }

        try:
            if self.id_horario is None:
                crear_horario(data)
                messagebox.showinfo("OK", "Horario registrado.")
            else:
                actualizar_horario(self.id_horario, data)
                messagebox.showinfo("OK", "Horario actualizado.")

            self.cargar_tabla()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    # -------------------------------------------------------
    def eliminar(self):
        if self.id_horario is None:
            messagebox.showwarning("Aviso", "Seleccione un horario para eliminar.")
            return

        try:
            eliminar_horario(self.id_horario)
            messagebox.showinfo("OK", "Horario eliminado.")
            self.cargar_tabla()
            self.limpiar_form()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


# Pruebas individuales
if __name__ == "__main__":
    root = tk.Tk()
    app = HorariosForm(master=root)
    app.mainloop()
