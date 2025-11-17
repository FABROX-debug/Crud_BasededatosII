# main.py
# ---------------------------------------------
# Arranque con LOGIN → luego Menú principal
# ---------------------------------------------

import tkinter as tk
from ui.login import LoginWindow
from ui.dashboard import Dashboard
from ui.citas_form import CitasForm
from ui.pacientes_form import PacientesForm
from ui.medicos_form import MedicosForm
from utils.styles import apply_styles


# ---------------------------------------------
# Menú principal
# ---------------------------------------------
class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Sistema de Reserva de Citas Médicas")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        apply_styles(self.master)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(
            self.master,
            text="Sistema de Reserva de Citas Médicas",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Dashboard",
            width=20,
            command=self.abrir_dashboard
        ).grid(row=0, column=0, pady=5)

        tk.Button(
            btn_frame,
            text="Gestión de Citas",
            width=20,
            command=self.abrir_citas
        ).grid(row=1, column=0, pady=5)

        tk.Button(
            btn_frame,
            text="Ver Pacientes",
            width=20,
            command=self.abrir_pacientes
        ).grid(row=2, column=0, pady=5)

        tk.Button(
            btn_frame,
            text="Ver Médicos",
            width=20,
            command=self.abrir_medicos
        ).grid(row=3, column=0, pady=5)

        tk.Button(
            btn_frame,
            text="Salir",
            width=20,
            command=self.master.destroy
        ).grid(row=4, column=0, pady=15)

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
    root.resizable(False, False)
    MainMenu(master=root)
    root.mainloop()


# ---------------------------------------------
# Arranque inicial → LOGIN primero
# ---------------------------------------------
if __name__ == "__main__":
    login_root = tk.Tk()
    login_root.resizable(False, False)
    LoginWindow(master=login_root, on_login_success=iniciar_sistema)
    login_root.mainloop()
