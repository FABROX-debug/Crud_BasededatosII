# ui/login.py
# -----------------------------------------------------------
# Pantalla de LOGIN del sistema (Optimizada PRO)
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

from models.usuarios import validar_usuario
from utils.styles import apply_styles, BACKGROUND_COLOR, PRIMARY_COLOR

USUARIO_LOGEADO = None


class LoginWindow(tk.Frame):
    # -------------------------------------------------------
    def __init__(self, master=None, on_login_success=None):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success

        self.master.title("Iniciar Sesión - Sistema Citas Médicas")
        self.master.resizable(False, False)

        # Tamaño ventana
        self.ancho = 380
        self.alto = 280
        self.centrar_ventana()

        apply_styles(self.master)
        self.crear_widgets()

    # -------------------------------------------------------
    def centrar_ventana(self):
        self.master.update_idletasks()
        w, h = self.ancho, self.alto
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    # -------------------------------------------------------
    def crear_widgets(self):
        cont = tk.Frame(self.master, padx=18, pady=18, bg=BACKGROUND_COLOR)
        cont.pack(expand=True, fill="both")

        tk.Label(
            cont,
            text="Sistema de Reserva de Citas Médicas",
            font=("Segoe UI", 12, "bold"),
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
        ).pack(pady=(0, 10))

        card = ttk.Frame(cont, padding=16, style="Card.TFrame")
        card.pack(fill="both", expand=True)

        frm = tk.Frame(card, bg="white")
        frm.pack(pady=5)

        # DNI
        tk.Label(frm, text="Usuario (DNI):", bg="white").grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.txt_usuario = tk.Entry(frm, width=28)
        self.txt_usuario.grid(row=0, column=1, padx=5, pady=8)

        # Contraseña
        tk.Label(frm, text="Contraseña:", bg="white").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.txt_password = tk.Entry(frm, width=28, show="*")
        self.txt_password.grid(row=1, column=1, padx=5, pady=8)

        # Press Enter para login
        self.txt_usuario.bind("<Return>", lambda e: self.validar_login())
        self.txt_password.bind("<Return>", lambda e: self.validar_login())

        btn_login = ttk.Button(
            card,
            text="Iniciar Sesión",
            width=20,
            command=self.validar_login,
        )
        btn_login.pack(pady=(12, 6))

        tk.Label(
            card,
            text="* Ingrese sus credenciales para continuar.",
            font=("Segoe UI", 8),
            fg="gray",
            bg="white",
        ).pack()

    # -------------------------------------------------------
    def validar_login(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        # Validaciones
        if usuario == "" or password == "":
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        if not usuario.isdigit() or len(usuario) != 8:
            messagebox.showwarning("DNI inválido", "El DNI debe contener 8 dígitos.")
            return

        # Consultar al modelo
        try:
            resultado = validar_usuario(usuario, password)
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar usuario:\n{e}")
            return

        if len(resultado) == 0:
            messagebox.showerror("Acceso denegado", "Credenciales inválidas o usuario inactivo.")
            return

        user_id, nombre, tipo = resultado[0]

        global USUARIO_LOGEADO
        USUARIO_LOGEADO = {
            "id": user_id,
            "nombre": nombre,
            "tipo": tipo,
        }

        # Mensaje amigable
        rol_texto = {
            "ADMIN": "Administrador",
            "MEDICO": "Médico",
            "PACIENTE": "Paciente"
        }.get(tipo, "Usuario")

        messagebox.showinfo("Bienvenido", f"¡Hola {nombre}! ({rol_texto})")

        self.master.destroy()

        # Redirigir al menú principal
        if self.on_login_success:
            self.on_login_success()
