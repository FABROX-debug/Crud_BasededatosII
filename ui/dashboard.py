# ui/dashboard.py
# -----------------------------------------------------------
# DASHBOARD PROFESIONAL — Sistema de Citas Médicas
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk

from models.citas import listar_citas
from models.medicos import listar_medicos
from models.pacientes import listar_pacientes


class Dashboard(tk.Frame):

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Dashboard - Sistema de Citas Médicas")
        self.master.geometry("1100x700")

        self.crear_widgets()
        self.cargar_estadisticas()
        self.cargar_citas()

    # -------------------------------------------------------
    def crear_widgets(self):

        tk.Label(
            self.master,
            text="Dashboard General",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # CONTENEDOR PRINCIPAL
        cont = tk.Frame(self.master)
        cont.pack(fill="both", expand=True, padx=10, pady=10)

        # -------------------------------------------------------
        # TARJETAS DE ESTADÍSTICAS
        # -------------------------------------------------------
        cards_frame = tk.Frame(cont)
        cards_frame.pack(fill="x")

        self.card_total_citas = self.crear_tarjeta(cards_frame, "Total de Citas", "0", "#1976D2")
        self.card_citas_hoy = self.crear_tarjeta(cards_frame, "Citas de Hoy", "0", "#388E3C")
        self.card_medicos = self.crear_tarjeta(cards_frame, "Médicos Activos", "0", "#7B1FA2")
        self.card_pacientes = self.crear_tarjeta(cards_frame, "Pacientes Registrados", "0", "#E64A19")

        # -------------------------------------------------------
        # TABLA DE PRÓXIMAS CITAS
        # -------------------------------------------------------
        tabla_frame = tk.Frame(cont)
        tabla_frame.pack(fill="both", expand=True, pady=15)

        tk.Label(
            tabla_frame,
            text="Próximas Citas",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        columnas = ("ID", "Paciente", "Médico", "Especialidad", "Fecha", "Horario", "Motivo", "Registrado")

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=18
        )

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=60)
        self.tree.column("Paciente", width=150)
        self.tree.column("Médico", width=150)
        self.tree.column("Especialidad", width=130)
        self.tree.column("Fecha", width=100)
        self.tree.column("Horario", width=140)
        self.tree.column("Motivo", width=180)
        self.tree.column("Registrado", width=130)

        self.tree.pack(fill="both", expand=True, pady=10)

    # -------------------------------------------------------
    def crear_tarjeta(self, parent, titulo, valor_inicial, color):
        """Crea tarjetas estadísticas del dashboard."""

        frame = tk.Frame(parent, bg=color, width=240, height=100)
        frame.pack(side="left", padx=10, pady=10)
        frame.pack_propagate(False)

        tk.Label(frame, text=titulo, font=("Segoe UI", 12, "bold"), bg=color, fg="white").pack()
        lbl = tk.Label(frame, text=valor_inicial, font=("Segoe UI", 26, "bold"), bg=color, fg="white")
        lbl.pack()

        return lbl

    # -------------------------------------------------------
    def cargar_estadisticas(self):
        citas = listar_citas()
        medicos = listar_medicos()
        pacientes = listar_pacientes()

        # Total de citas
        self.card_total_citas["text"] = len(citas)

        # Citas del día
        citas_hoy = [c for c in citas if c[4] == self.fecha_hoy()]
        self.card_citas_hoy["text"] = len(citas_hoy)

        # Médicos activos
        med_activos = [m for m in medicos if m[4] == "S"]
        self.card_medicos["text"] = len(med_activos)

        # Pacientes total
        self.card_pacientes["text"] = len(pacientes)

    # -------------------------------------------------------
    def fecha_hoy(self):
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d")

    # -------------------------------------------------------
    def cargar_citas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        citas = listar_citas()

        # Ordenar por fecha
        citas_ordenadas = sorted(citas, key=lambda x: (x[4], x[5]))

        for c in citas_ordenadas:
            self.tree.insert("", tk.END, values=c)


# PRUEBA AISLADA
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(master=root)
    root.mainloop()
