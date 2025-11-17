# ui/login.py
# -----------------------------------------------------------
# Pantalla de LOGIN del sistema
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from db_oracle import fetch_all
from utils.styles import apply_styles


class LoginWindow(tk.Frame):
    def __init__(self, master=None, on_login_success=None):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success

        self.master.title("Iniciar Sesión")
        self.master.geometry("350x250")
        self.master.resizable(False, False)

        apply_styles(self.master)
        self.crear_widgets()

    # -------------------------------------------------------
    def crear_widgets(self):
        tk.Label(
            self.master,
            text="Ingreso al Sistema",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)

        cont = tk.Frame(self.master)
        cont.pack(pady=10)

        tk.Label(cont, text="Usuario (DNI):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_usuario = tk.Entry(cont, width=25)
        self.txt_usuario.grid(row=0, column=1)

        tk.Label(cont, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_password = tk.Entry(cont, width=25, show="*")
        self.txt_password.grid(row=1, column=1)

        tk.Button(
            self.master,
            text="Iniciar Sesión",
            width=20,
            command=self.validar_login
        ).pack(pady=15)

    # -------------------------------------------------------
    def validar_login(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        if usuario == "" or password == "":
            messagebox.showwarning("Aviso", "Complete todos los campos.")
            return

        # Validamos en Oracle
        query = """
            SELECT ID_USUARIO, NOMBRE_COMPLETO, TIPO_USUARIO
            FROM USUARIO
            WHERE DNI = :dni
              AND CORREO = :password    -- puedes cambiarlo por un campo PASSWORD real
              AND ESTADO_ACTIVO = 'S'
        """

        params = {"dni": usuario, "password": password}
        resultado = fetch_all(query, params)

        if len(resultado) == 0:
            messagebox.showerror("Error", "Credenciales incorrectas o usuario inactivo.")
            return

        # Login correcto
        datos_user = resultado[0]
        user_id, nombre, tipo = datos_user

        # Guardamos el usuario en una variable global
        global USUARIO_LOGEADO
        USUARIO_LOGEADO = {
            "id": user_id,
            "nombre": nombre,
            "tipo": tipo
        }

        messagebox.showinfo("Bienvenido", f"Hola {nombre}!")

        self.master.destroy()  # Cerrar login
        if self.on_login_success:
            self.on_login_success()
