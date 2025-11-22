# ui/dashboard.py
# -----------------------------------------------------------
# DASHBOARD PROFESIONAL — Sistema de Citas Médicas
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk

from models.citas import listar_citas
from models.medicos import listar_medicos
from models.pacientes import listar_pacientes
from utils.styles import BACKGROUND_COLOR


class Dashboard(tk.Frame):

    # -------------------------------------------------------
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=BACKGROUND_COLOR)
        self.master.configure(bg=BACKGROUND_COLOR)

        self.master.title("Dashboard - Sistema de Citas Médicas")
        self.master.geometry("1100x700")

        self.crear_widgets()
        self.cargar_estadisticas()
        self.cargar_citas()

    # -------------------------------------------------------
    # -------------------------------------------------------
    def crear_widgets(self):

        # Header
        header_frame = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ttk.Label(
            header_frame,
            text="Dashboard General",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Resumen de actividad del sistema",
            style="Subtitle.TLabel"
        ).pack(anchor="w")

        # CONTENEDOR PRINCIPAL
        cont = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        cont.pack(fill="both", expand=True, padx=20, pady=10)

        # -------------------------------------------------------
        # TARJETAS DE ESTADÍSTICAS
        # -------------------------------------------------------
        cards_frame = tk.Frame(cont, bg=BACKGROUND_COLOR)
        cards_frame.pack(fill="x", pady=(0, 20))

        # Colores para las tarjetas (usando variables o hardcoded para variedad)
        self.card_total_citas = self.crear_tarjeta(cards_frame, "Total Citas", "0", "#3B82F6") # Blue 500
        self.card_citas_hoy = self.crear_tarjeta(cards_frame, "Citas Hoy", "0", "#10B981")   # Emerald 500
        self.card_medicos = self.crear_tarjeta(cards_frame, "Médicos", "0", "#8B5CF6")       # Violet 500
        self.card_pacientes = self.crear_tarjeta(cards_frame, "Pacientes", "0", "#F59E0B")   # Amber 500

        # -------------------------------------------------------
        # TABLA DE PRÓXIMAS CITAS
        # -------------------------------------------------------
        tabla_frame = ttk.Frame(cont, style="Card.TFrame", padding=20)
        tabla_frame.pack(fill="both", expand=True)

        ttk.Label(
            tabla_frame,
            text="Próximas Citas",
            font=("Segoe UI", 14, "bold"),
            background="white"
        ).pack(anchor="w", pady=(0, 15))

        columnas = ("ID", "Paciente", "Médico", "Especialidad", "Fecha", "Horario", "Motivo", "Registrado")

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=15,
            style="Treeview"
        )

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Paciente", width=150)
        self.tree.column("Médico", width=150)
        self.tree.column("Especialidad", width=120)
        self.tree.column("Fecha", width=90, anchor="center")
        self.tree.column("Horario", width=120, anchor="center")
        self.tree.column("Motivo", width=180)
        self.tree.column("Registrado", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # -------------------------------------------------------
    def crear_tarjeta(self, parent, titulo, valor_inicial, color):
        """Crea tarjetas estadísticas del dashboard."""
        
        # Contenedor de la tarjeta
        card = tk.Frame(parent, bg="white", width=220, height=110)
        card.pack(side="left", padx=(0, 20))
        card.pack_propagate(False)
        
        # Borde izquierdo de color
        border = tk.Frame(card, bg=color, width=6, height=110)
        border.pack(side="left", fill="y")
        
        # Contenido
        content = tk.Frame(card, bg="white", padx=15, pady=15)
        content.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            content, 
            text=titulo, 
            font=("Segoe UI", 10, "bold"), 
            bg="white", 
            fg="#6B7280" # Gray 500
        ).pack(anchor="w")
        
        lbl = tk.Label(
            content, 
            text=valor_inicial, 
            font=("Segoe UI", 24, "bold"), 
            bg="white", 
            fg="#111827" # Gray 900
        )
        lbl.pack(anchor="w")

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
