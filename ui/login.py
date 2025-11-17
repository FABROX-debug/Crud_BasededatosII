# ui/login.py
# -----------------------------------------------------------
# Pantalla de LOGIN del sistema
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from db_oracle import fetch_all
from utils.styles import apply_styles

# variable global opcional para guardar el usuario logueado
USUARIO_LOGEADO = None


class LoginWindow(tk.Frame):
    def __init__(self, master=None, on_login_success=None):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success

        self.master.title("Iniciar Sesión - Citas Médicas")
        self.master.resizable(False, False)

        # tamaño fijo de la ventana
        self.ancho = 360
        self.alto = 260
        self.centrar_ventana()

        apply_styles(self.master)
        self.crear_widgets()

    # -------------------------------------------------------
    def centrar_ventana(self):
        self.master.update_idletasks()
        w = self.ancho
        h = self.alto
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    # -------------------------------------------------------
    def crear_widgets(self):
        cont_principal = tk.Frame(self.master, padx=15, pady=15)
        cont_principal.pack(expand=True, fill="both")

        tk.Label(
            cont_principal,
            text="Sistema de Reserva de Citas Médicas",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(0, 10))

        frm = tk.Frame(cont_principal)
        frm.pack(pady=5)

        tk.Label(frm, text="Usuario (DNI):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_usuario = tk.Entry(frm, width=25)
        self.txt_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_password = tk.Entry(frm, width=25, show="*")
        self.txt_password.grid(row=1, column=1, padx=5, pady=5)

        btn_login = ttk.Button(
            cont_principal,
            text="Iniciar Sesión",
            width=20,
            command=self.validar_login
        )
        btn_login.pack(pady=(10, 5))

        tk.Label(
            cont_principal,
            text="* Por ahora la contraseña es el correo registrado.",
            font=("Segoe UI", 8),
            fg="gray"
        ).pack()

    # -------------------------------------------------------
    def validar_login(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        if usuario == "" or password == "":
            messagebox.showwarning("Aviso", "Complete todos los campos.")
            return

        query = """
            SELECT ID_USUARIO, NOMBRE_COMPLETO, TIPO_USUARIO
            FROM USUARIO
            WHERE DNI = :dni
              AND CORREO = :password
              AND ESTADO_ACTIVO = 'S'
        """
        params = {"dni": usuario, "password": password}
        resultado = fetch_all(query, params)

        if len(resultado) == 0:
            messagebox.showerror("Error", "Credenciales incorrectas o usuario inactivo.")
            return

        user_id, nombre, tipo = resultado[0]

        global USUARIO_LOGEADO
        USUARIO_LOGEADO = {
            "id": user_id,
            "nombre": nombre,
            "tipo": tipo
        }

        messagebox.showinfo("Bienvenido", f"Hola {nombre}!")
        self.master.destroy()

        if self.on_login_success:
            self.on_login_success()
