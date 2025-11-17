# main.py
# ---------------------------------------------
# Arranque con LOGIN → luego Menú principal
# ---------------------------------------------

import tkinter as tk
from tkinter import ttk
from ui.login import LoginWindow
from ui.dashboard import Dashboard
from ui.citas_form import CitasForm
from ui.pacientes_form import PacientesForm
from ui.medicos_form import MedicosForm
from utils.styles import apply_styles, BACKGROUND_COLOR, PRIMARY_COLOR


class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Sistema de Reserva de Citas Médicas")
        self.master.resizable(False, False)

        self.ancho = 440
        self.alto = 340
        self.centrar_ventana()

        apply_styles(self.master)
        self.crear_widgets()

    def centrar_ventana(self):
        self.master.update_idletasks()
        w = self.ancho
        h = self.alto
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    def crear_widgets(self):
        cont = tk.Frame(self.master, padx=20, pady=20, bg=BACKGROUND_COLOR)
        cont.pack(expand=True, fill="both")

        header = tk.Frame(cont, bg=BACKGROUND_COLOR)
        header.pack(pady=(0, 10))
        tk.Label(
            header,
            text="Sistema de Reserva de Citas Médicas",
            font=("Segoe UI", 15, "bold"),
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
        ).pack()
        tk.Label(
            header,
            text="Menú principal",
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR,
        ).pack()

        card = ttk.Frame(cont, style="Card.TFrame", padding=18)
        card.pack(expand=True, fill="both")

        botones = [
            ("Dashboard", self.abrir_dashboard),
            ("Gestión de Citas", self.abrir_citas),
            ("Ver Pacientes", self.abrir_pacientes),
            ("Ver Médicos", self.abrir_medicos),
            ("Salir", self.master.destroy),
        ]

        for i, (texto, comando) in enumerate(botones):
            ttk.Button(
                card,
                text=texto,
                width=22,
                command=comando,
            ).grid(row=i, column=0, pady=6, padx=5)

    # -----------------------------
    # VENTANAS SECUNDARIAS
    # -----------------------------
    def abrir_dashboard(self):
        window = tk.Toplevel(self.master)
        Dashboard(master=window)

    def abrir_citas(self):
        window = tk.Toplevel(self.master)
        CitasForm(master=window)

    def abrir_pacientes(self):
        window = tk.Toplevel(self.master)
        PacientesForm(master=window)

    def abrir_medicos(self):
        window = tk.Toplevel(self.master)
        MedicosForm(master=window)


# ---------------------------------------------
# INICIAR LA APLICACIÓN TRAS LOGIN EXITOSO
# ---------------------------------------------
def iniciar_sistema():
    root = tk.Tk()
    MainMenu(master=root)
    root.mainloop()


# ---------------------------------------------
# Arranque inicial → LOGIN primero
# ---------------------------------------------
if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(master=login_root, on_login_success=iniciar_sistema)
    login_root.mainloop()
